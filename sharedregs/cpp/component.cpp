///////////////////////////////////////////////////////////////////////////////
//
//  Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are met:
//
//  1. Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//  2. Redistributions in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
//  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
//  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
//  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
//  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
//  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
//  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
//  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
//  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
//  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
//  POSSIBILITY OF SUCH DAMAGE.
//
///////////////////////////////////////////////////////////////////////////////

#include <string>
#include <iostream>

#include "autobahn.hpp"

#include <boost/asio.hpp>
#include <boost/version.hpp>

using namespace std;
using namespace boost;
using namespace autobahn;

using boost::asio::ip::tcp;

#include <unistd.h>


any add2(const anyvec& args, const anymap& kwargs) {

   double x = any_cast<double> (args[0]);
   double y = any_cast<double> (args[1]);

   std::stringstream ident;
   ident << "<PID: " << getpid() << ">";

   cerr << "add2() " << ident.str() << " called with "
      << x << " and " << y << endl;

   anymap res;
   res["result"] = any(x + y);
   res["ident"] = ident.str();

   return res;
}


int main () {

   cerr << "Running on " << BOOST_VERSION << endl;

   try {
      // ASIO service object
      //
      asio::io_service io;

      // the TCP socket we connect
      //
//      tcp::socket socket(io);
      tcp::socket socket(io, tcp::v4());

      // setting this option minimizes latency at some cost
      //
      socket.set_option(tcp::no_delay(true));

      // connect to this server/port
      //
      tcp::resolver resolver(io);
      auto endpoint_iterator = resolver.resolve({"localhost", "8090"});

      // create a WAMP session that talks over TCP
      //
      bool debug = false;
      autobahn::session<tcp::socket,
                        tcp::socket> session(io, socket, socket, debug);

      // make sure the future returned from the session joining a realm (see below)
      // does not run out of scope (being destructed prematurely ..)
      //
      future<void> session_future;

      // now do an asynchronous connect ..
      //
      boost::asio::async_connect(socket, endpoint_iterator,

         // we either connected or an error happened during connect ..
         //
         [&](boost::system::error_code ec, tcp::resolver::iterator) {

            if (!ec) {
               cerr << "Connected to server" << endl;

               // start the WAMP session on the transport that has been connected
               //
               session.start();

               // join a realm with the WAMP session
               //
               session_future = session.join("realm1").then([&](future<uint64_t> s) {

                  cerr << "Session joined to realm with session ID " << s.get() << endl;

                  // REGISTER a procedure for remote calling
                  //
                  autobahn::anymap options;
                  options["invoke"] = std::string("roundrobin");
                  //options["invoke"] = std::string("random");
                  //options["invoke"] = std::string("first");
                  //options["invoke"] = std::string("last");

                  auto r1 = session.provide("com.example.add2", static_cast<endpoint_t>(&add2), options);

                  r1.then([](future<registration> reg) {
                     cerr << "procedure add2() registered with registration ID " << reg.get().id << endl;
                  }).wait();
               });

            } else {
               cerr << "Could not connect to server: " << ec.message() << endl;
            }
         }
      );

      cerr << "Starting ASIO I/O loop .." << endl;

      io.run();

      cerr << "ASIO I/O loop ended" << endl;
   }
   catch (std::exception& e) {
      cerr << e.what() << endl;
      return 1;
   }
   return 0;
}
