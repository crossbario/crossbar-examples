Test topology:

* [node1](http://localhost:8001)
  * [node2](http://localhost:8002)
    * [node4](http://localhost:8004)
    * [node5](http://localhost:8005)
  * [node3](http://localhost:8003)

```
node1
  |
  +-- node2
  |     |
  |     +-- node4
  |     |
  |     +-- node5
  |
  +-- node3
```






Allocate a new Elastic IP address with scope VPC

Create a Network Load Balancer 
 - Internet-facing
 - Load Balancer Protocol TCP
 - Ports 80, 443, 8080




https://cloud-images.ubuntu.com/locator/ec2/

`ami-0dfd7cad24d571c54`

```
Zone 	        Name 	  Version 	  Arch 	  Instance Type 	      Release 	AMI-ID 	      AKI-ID
-------------------------------------------------------------------------------------------------------------------
eu-central-1	bionic	18.04 LTS	  amd64	  hvm:ebs-ssd	20181012  ami-07b0dc14c4fdcf6c6	  hvm
```


m5.large
	
2 VCPUs, 8GB RAM, EBS, 10 Gigabit
~70 USD/month
