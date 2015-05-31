# -*- coding: utf-8 -*-

###############################################################################
##
##  Copyright (C) 2014 Michel Desmoulin
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################


from autobahn.twisted.wamp import Application

import socket
import uuid

# Comme pour flask, l'objet app
# est ce qui lie tous les éléments
# de notre code ensemble. On lui donne
# un nom, ici "demo"
app = Application('io.crossbar.demo.videocontroller')
# Bien que l'app va démarrer un serveur
# pour nous, l'app est bien un CLIENT
# du serveur WAMP. Le serveur démarré
# automatiquement n'est qu'une facilité
# pour le dev. En prod on utiliserait
# crossbar.

# Juste un conteneur pour y mettre notre IP
app._data = {}

# On déclare que cette fonction sera appelée
# quand l'app se sera connectée au serveur WAMP.
# Ceci permet de lancer du code juste après
# le app.run() que l'on voit en bas du fichier.
# '_' est une convention en Python pour dire
# "ce nom n'a aucune importance, c'est du code
# jetable qu'un utilisera une seule fois".
@app.signal('onjoined')
def _():
   # On récupère notre adresse IP sur le réseau local
   # C'est une astuce qui se connecte à un DNS, et donc
   # on a besoin d'une connexion internet.
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))
   # On stocke l'adresse IP locale dans un conteneur
   # qui sera accessible partout ailleur.
   app._data['LOCAL_IP'] = s.getsockname()[0]
   s.close()

# On déclare que la fonciton "ip()" est appelable
# via RCP. Ce qui veut dire que tout autre client
# WAMP peut obtenir le résultat de cette fonction.
# Donc on va pouvoir l'appeler depuis notre navigateur.
# Comme notre app s'appelle "io.crossbar.demo.videocontroller" et notre fonction
# s'appelle "ip", un client pourra l'appeler en faisant
# "io.crossbar.demo.videocontroller.ip".
@app.register()
def ip():
   # On ne fait que retourner l'IP locale. Rien de fou.
   return app._data['LOCAL_IP']

# Je voulais appeler cette fonction distante "uuid", mais ça
# override le module Python uuid. Ce n'est pas une bonne
# idée. Je l'appelle donc 'get_uuid' mais je déclare le
# nom complet dans register(). Un client WAMP pourra donc
# bien l'appeler via "io.crossbar.demo.videocontroller.uuid".
# Notez que ce namespace doit toujours s'écrire
# truc.machine.bidule. Pas truc/machin ou truc:machin.
# ou truc et bidule.MACHIN.
@app.register('io.crossbar.demo.videocontroller.uuid')
def get_uuid():
   # Retourne un UUID, sans les tirets.
   # ex: b27f7e9360c04efabfae5ac21a8f4e3c
   return str(uuid.uuid4()).replace('-', '')

# On lance l'application. Ceci va lancer le serveur
# puis le client. On peut désactiver le lancement du
# serveur une fois qu'on met tout ça en prod.
if __name__ == "__main__":
   app.run(url = "ws://0.0.0.0:8080/")
   # On ne peut rien mettre comme code ici, il faut le
   # mettre dans @app.signal('onjoined') si on veut
   # entrer du code après que l'app soit lancée.
