from urllib.request import urlopen
import lxml.html
import re

def garbitu (string):
	string = string.replace('&nbsp', ' ')
	string = re.sub(r'[ \t\n\r]+', ' ', string)
	return string.strip()
	
def idatzi_garbia (string, fitx):
	garbia = garbitu(string)
	fitx.write(garbia + '\n')

link = 'https://www.ehu.eus/ehg/hac/liburua'
f = urlopen(link)
liburuak_html = f.read()
root = lxml.html.fromstring(liburuak_html)
elems = root.cssselect('span.tituloak')
liburu_linkak = [elem.getchildren()[0].attrib['href'] for elem in elems]
liburu_linkak.pop(-6) # Voltairen esteka ez dabil

or_kopuruak = []
for i, lib_link in enumerate(liburu_linkak):
	print(i, lib_link)
	link = 'https://www.ehu.eus/ehg/hac/'+lib_link
	f = urlopen(link)
	orria1_html = f.read()
	root = lxml.html.fromstring(orria1_html)
	elems = root.cssselect('div.nabi')
	or_kop = elems[0].text_content().split()[0]
	or_kopuruak.append(int(or_kop))

fitx_eu = open('EhuHac-eu.txt', 'a')
fitx_es = open('EhuHac-es.txt', 'a')
fitx_fr = open('EhuHac-fr.txt', 'a')
fitx_en = open('EhuHac-en.txt', 'a')

hasi_lib = int(input('Sartu lehen liburuaren zenbakia (0tik hasita): '))
hasi_or = int(input('Sartu lehen orriaren zenbakia (1etik hasita): '))

for lib_link, or_kop in zip(liburu_linkak[hasi_lib:], or_kopuruak[hasi_lib:]):
	for orria in range(hasi_or, or_kop+1):
		link = 'https://www.ehu.eus/ehg/hac/'+lib_link+'&o='+str(orria)
		print(link+'               ', end='\r')
		f = urlopen(link)
		orria_html = f.read()
		deskodetuta = orria_html.decode('windows-1252')
		root = lxml.html.fromstring(deskodetuta)
		launaka = root.cssselect('div.esal ')
		for esaldia in launaka:
			bakoitza = esaldia.cssselect('div.esalBi')
			idatzi_garbia(bakoitza[0].text_content(), fitx_eu)
			idatzi_garbia(bakoitza[1].text_content(), fitx_es)
			idatzi_garbia(bakoitza[2].text_content(), fitx_fr)
			idatzi_garbia(bakoitza[3].text_content(), fitx_en)
	hasi_or = 1
	# LIBURUAREN BUKAERA MARKA JARTZEKO, HEMEN
				
print()
fitx_eu.close()
fitx_es.close()
fitx_fr.close()
fitx_en.close()