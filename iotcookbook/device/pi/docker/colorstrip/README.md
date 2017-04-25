dpipe /usr/lib/openssh/sftp-server = ssh $REMOTE_HOST sshfs whatever:$LOCAL_PATH $REMOTE_PATH -o slave

dpipe /usr/lib/openssh/sftp-server = ssh pi@192.168.55.133 sshfs :/home/oberstet/scm /home/pi/scm -o slave

https://blog.dhampir.no/content/reverse-sshfs-mounts-fs-push
