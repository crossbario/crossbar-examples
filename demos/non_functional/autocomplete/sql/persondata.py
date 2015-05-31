import fileinput, json, pprint, sys, re

class Person:
   def __init__(self, uri):
      self.uri = uri
      self.name = None
      self.surname = None
      self.givenname = None
      self.description = None
      self.birthdate = None
      self.birthplace = []
      self.deathdate = None
      self.deathplace = []

   def csv(self):
      descr = None
      if self.description:
         if len(self.description) > 1000:
            descr = self.description[:1000] + ' ..'
         else:
            descr = self.description

      if self.surname and self.givenname:
         name = "%s, %s" % (self.surname, self.givenname)
      else:
         n = [x.strip() for x in self.name.split()]
         if len(n) > 1:
            name = "%s, %s" % (n[0], ' '.join(n[1:]))
         else:
            name = n[0]

      if self.surname:
         if self.givenname:
            sname = "%s %s" % (self.surname, self.givenname)
         else:
            sname = self.surname
      else:
         sname = name.replace(',', '')
      sname = sname.lower()

      l = [sname,
           self.uri,
           name,
           self.surname,
           self.givenname,
           self.birthdate,
           ', '.join(self.birthplace) if len(self.birthplace) > 0 else None,
           self.deathdate,
           ', '.join(self.deathplace) if len(self.deathplace) > 0 else None,
           descr]

      l = ['"%s"' % x.encode("utf-8") if x is not None else '' for x in l]

      #return sname.encode("utf-8") + ';' + str(self.id) + ';' + ';'.join(l)
      return ';'.join(l)

   def get(self):
      return {'id': self.id,
              'uri': self.uri,
              'name': self.name,
              'surname': self.surname,
              'givenname': self.givenname,
              'description': self.description,
              'deathdate': self.deathdate,
              'birthdate': self.birthdate,
              'deathplace': ', '.join(self.deathplace) if len(self.deathplace) > 0 else None,
              'birthplace': ', '.join(self.birthplace) if len(self.birthplace) > 0 else None}

   def __repr__(self):
      return json.dumps(self.get())


def getlabel(s):
   s = s.decode('utf-8').replace(";", ",")
   return s.split('"')[1]

def getplace(s):
   s = s.decode('utf-8').replace(";", ",")
   return s.split('/')[-1].replace('_', ' ')


def processfile(infile, outfile, format = "csv", max = None, debug = False):
   person = None
   n = 0

   of = open(outfile, 'w')

   datepat = re.compile("\d\d\d\d-\d\d-\d\d")

   for line in fileinput.input([infile]):
      r = [x.strip() for x in line.strip().split('>')]
      if len(r) >= 3:
         uri = r[0][1:].decode('utf-8')
         if person is None or uri != person.uri:
            if person:
               n += 1
               if max and n > max:
                  return

               person.id = n

               if format == "csv":
                  of.write(person.csv())
               elif format == "json":
                  of.write(str(person))
               else:
                  raise Exception("invalid format")
               of.write('\n')

               sys.stdout.write(".")
               if debug:
                  pprint.pprint(person.get())

            person = Person(uri)

         if debug:
            print r

         if r[1] == '<http://xmlns.com/foaf/0.1/name':
            person.name = getlabel(r[2])
         elif r[1] == '<http://xmlns.com/foaf/0.1/surname':
            person.surname = getlabel(r[2])
         elif r[1] == '<http://xmlns.com/foaf/0.1/givenName':
            person.givenname = getlabel(r[2])
         elif r[1] == '<http://purl.org/dc/elements/1.1/description':
            person.description = getlabel(r[2])
         elif r[1] == '<http://dbpedia.org/ontology/birthDate':
            person.birthdate = getlabel(r[2])
            if not datepat.match(person.birthdate):
               person.birthdate = None
         elif r[1] == '<http://dbpedia.org/ontology/deathDate':
            person.deathdate = getlabel(r[2])
            if not datepat.match(person.deathdate):
               person.deathdate = None
         elif r[1] == '<http://dbpedia.org/ontology/birthPlace':
            person.birthplace.append(getplace(r[2]))
         elif r[1] == '<http://dbpedia.org/ontology/deathPlace':
            person.deathplace.append(getplace(r[2]))

if len(sys.argv) < 3:
   print "Usage: python process_persondata.py <input file> <output file>"
   sys.exit(1)

processfile(sys.argv[1], sys.argv[2])
