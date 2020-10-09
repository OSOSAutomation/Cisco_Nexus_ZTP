x= cli('show running-config | include address')
y= x.find('192.168.101.191/25')
z= x.find('192.168.101.192/25')
if y != -1:
    cli ('copy tftp://192.168.101.253/initdev1.cfg bootflash: vrf management')
    cli ('copy bootflash:initdev1.cfg scheduled-config')
if z != -1:
    cli ('copy tftp://192.168.101.253/initdev2.cfg bootflash: vrf management')
    cli ('copy bootflash:initdev2.cfg scheduled-config')
cli ('copy running-config startup-config')
