<?php
/******************************************************************************
**
**  Copyright 2012 Tavendo GmbH
**
**  Licensed under the Apache License, Version 2.0 (the "License");
**  you may not use this file except in compliance with the License.
**  You may obtain a copy of the License at
**
**      http://www.apache.org/licenses/LICENSE-2.0
**
**  Unless required by applicable law or agreed to in writing, software
**  distributed under the License is distributed on an "AS IS" BASIS,
**  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
**  See the License for the specific language governing permissions and
**  limitations under the License.
**
******************************************************************************/

function urlsafe_b64encode($string)
{
   $data = base64_encode($string);
   $data = str_replace(array('+','/'),array('-','_'),$data);
   return $data;
}


class WebMQConnectClient
{
   private $opts = array ();
   private $ch = null;

   public function __construct($pushendpoint, $authkey = null, $authsecret = null, $timeout = 5)
   {
      $this->opts['pushendpoint'] = $pushendpoint;

      if (trim($authkey) == "") {
         $authkey = null;
         $authsecret = null;
      }

      $this->opts['authkey'] = $authkey;
      $this->opts['authsecret'] = $authsecret;
      $this->opts['timeout'] = $timeout;

      $this->ch = curl_init();
      if ($this->ch === false)
      {
         die('Fatal: cURL could not be initialized.');
      }

      curl_setopt($this->ch, CURLOPT_HTTPHEADER, array("Content-Type: application/x-www-form-urlencoded", "User-Agent: WebMQConnectPHP") );
      curl_setopt($this->ch, CURLOPT_RETURNTRANSFER, 1);
      curl_setopt($this->ch, CURLOPT_POST, 1);
      curl_setopt($this->ch, CURLOPT_TIMEOUT, $this->opts['timeout']);
   }

   public function __destruct() {
      curl_close($this->ch);
      $this->ch = null;
   }

   public function push($topic, $event, $eligible = null, $exclude = null)
   {
      $msg = json_encode($event);

      $data = array('topicuri' => $topic);
      if ($this->opts['authkey'] !== null)
      {
         $timestamp = gmdate("Y-m-d\TH:i:s\Z");
         $sig = urlsafe_b64encode(hash_hmac('sha256', $topic . $this->opts['authkey'] . $timestamp . $msg, $this->opts['authsecret'], true));
         $data['timestamp'] = $timestamp;
         $data['appkey'] = $this->opts['authkey'];
         $data['signature'] = $sig;
      }
      if ($eligible !== null)
      {
         $data['eligible'] = join(',', $eligible);
      }
      if ($exclude !== null)
      {
         $data['exclude'] = join(',', $exclude);
      }

      $url = $this->opts['pushendpoint'] . '/?' . http_build_query($data, '', '&');

      curl_setopt($this->ch, CURLOPT_URL, $url);
      curl_setopt($this->ch, CURLOPT_POSTFIELDS, $msg);

      $response = curl_exec($this->ch);
      $status_code = curl_getinfo($this->ch, CURLINFO_HTTP_CODE);

      if ($status_code !== 202)
      {
         return $response;
      }
      else
      {
         return null;
      }
   }
}

/**
 * Lookup if browser supports WebSocket (Hixie76, Hybi10+, RFC6455) natively,
 * and if not, whether the web-socket-js Flash bridge works to polyfill that.
 *
 * Returns an array:
 *
 *   ws_supported       WebSocket is supported
 *   needs_flash        Flash Bridge is needed for support
 *   needs_hixie76      WebSocket Hixie-76 support is needed
 *   detected           The code has explicitly mapped the support/nosupport
 */
function lookupWsSupport($ua = null)
{
   if ($ua === null) {
      $ua = $_SERVER['HTTP_USER_AGENT'];
   }

   // ws_supported, needs_flash, detected
   $ws = array();
   $ws['user_agent'] = $ua;

   // Internet Explorer
   //
   if (preg_match("*MSIE*", $ua)) {

      // IE10 has native support
      if (preg_match("*MSIE 10*", $ua)) {
         $ws['ws_supported'] = true;
         $ws['needs_flash'] = false;
         $ws['needs_hixie76'] = false;
         $ws['detected'] = true;
         $ws['browser'] = 'IE10';
         return $ws;
      }

      // Google Chrome Frame
      if (preg_match("*chromeframe*", $ua)) {
         $ws['ws_supported'] = true;
         $ws['needs_flash'] = false;
         $ws['needs_hixie76'] = false;
         $ws['detected'] = true;
         $ws['browser'] = 'IE with Chrome Frame';
         return $ws;
      }

      // Flash fallback
      if (preg_match("*MSIE 8*", $ua) || preg_match("*MSIE 9*", $ua)) {
         $ws['ws_supported'] = true;
         $ws['needs_flash'] = true;
         $ws['needs_hixie76'] = false;
         $ws['detected'] = true;
         $ws['browser'] = 'IE8/9';
         return $ws;
      }

      // unsupported
      $ws['ws_supported'] = false;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = false;
      $ws['detected'] = true;
      $ws['browser'] = 'IE/Unsupported';
      return $ws;
   }

   // iOS
   //
   if (preg_match("*iPhone*", $ua) || preg_match("*iPad*", $ua) || preg_match("*iPod*", $ua)) {
      $ws['ws_supported'] = true;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = true;
      $ws['detected'] = true;
      $ws['browser'] = 'WebKit/iOS';
      return $ws;
   }

   // Android
   //
   if (preg_match("*Android*", $ua)) {

      // Firefox Mobile
      if (preg_match("*Firefox*", $ua)) {
         $ws['ws_supported'] = true;
         $ws['needs_flash'] = false;
         $ws['needs_hixie76'] = false;
         $ws['detected'] = true;
         $ws['browser'] = 'Firefox Mobile';
         return $ws;
      }

      // Opera Mobile
      if (preg_match("*Opera*", $ua)) {
         $ws['ws_supported'] = true;
         $ws['needs_flash'] = false;
         $ws['needs_hixie76'] = true;
         $ws['detected'] = true;
         $ws['browser'] = 'Opera Mobile';
         return $ws;
      }

      // Chrome for Android
      if (preg_match("*CoMo*", $ua)) {
         $ws['ws_supported'] = true;
         $ws['needs_flash'] = false;
         $ws['needs_hixie76'] = false;
         $ws['detected'] = true;
         $ws['browser'] = 'Chrome for Android';
         return $ws;
      }

      // Android builtin browser
      if (preg_match("*AppleWebKit*", $ua)) {
         $ws['ws_supported'] = true;
         $ws['needs_flash'] = true;
         $ws['needs_hixie76'] = false;
         $ws['detected'] = true;
         $ws['browser'] = 'Android/Builtin';
         return $ws;
      }

      // detection problem
      $ws['ws_supported'] = false;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = false;
      $ws['detected'] = false;
      $ws['browser'] = 'Undetected';
      return $ws;
   }

   // webOS
   //
   if (preg_match("*hpwOS*", $ua) || preg_match("*webos*", $ua)) {
      $ws['ws_supported'] = true;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = true;
      $ws['detected'] = true;
      $ws['browser'] = 'WebKit/webOS';
      return $ws;
   }

   // Opera
   //
   if (preg_match("*Opera*", $ua)) {
      $ws['ws_supported'] = true;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = true;
      $ws['detected'] = true;
      $ws['browser'] = 'Opera';
      return $ws;
   }

   // Firefox
   //
   if (preg_match("*Firefox*", $ua)) {
      $ws['ws_supported'] = true;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = false;
      $ws['detected'] = true;
      $ws['browser'] = 'Firefox';
      return $ws;
   }

   // Safari
   //
   if (preg_match("*Safari*", $ua) && !preg_match("*Chrome*", $ua)) {
      $ws['ws_supported'] = true;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = true;
      $ws['detected'] = true;
      $ws['browser'] = 'Safari';
      return $ws;
   }

   // Chrome
   //
   if (preg_match("*Chrome*", $ua)) {
      $ws['ws_supported'] = true;
      $ws['needs_flash'] = false;
      $ws['needs_hixie76'] = false;
      $ws['detected'] = true;
      $ws['browser'] = 'Chrome';
      return $ws;
   }

   // detection problem
   //
   $ws['ws_supported'] = false;
   $ws['needs_flash'] = false;
   $ws['needs_hixie76'] = false;
   $ws['detected'] = false;
   $ws['browser'] = 'Undetected';
}

?>
