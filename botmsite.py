# -- coding: utf-8 --
import time, smtplib, os, pyscreenshot, openpyxl
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait	
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


servicedesk_email = "servicedesk.robo2@gmail.com"
servicedesk_password = "Sd2019monitoracao"



def comprar(url, site):

	browser.get("https://secure.{}.com.br/customer/account/login/".format(site))

	#login e senha para entrar no site
	#espera 10 segundos pelo elemento
	WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH,"""//*[@id="LoginForm_email"]""")))

	browser.find_element_by_xpath("""//*[@id="LoginForm_email"]""").send_keys(servicedesk_email)
	time.sleep(0.5)
	browser.find_element_by_xpath("""//*[@id="LoginForm_password"]""").send_keys(servicedesk_password)
	time.sleep(0.5)
	browser.find_element_by_xpath("""//*//*[@id="send-2"]""").click()
	time.sleep(4)

	#abre um item
	browser.get(url)
	time.sleep(8)

	try:
		browser.find_element_by_class_name("""hide-box-button""").click()
		time.sleep(3)
	except NoSuchElementException:
		pass
		
	#popup de pesquisa rapida
	browser.find_element_by_xpath("""//*[@id="add-to-cart"]/div/div[3]/button""").click()
	time.sleep(3)
	browser.get("https://secure.{}.com.br/cart/".format(site))
	time.sleep(8)

	#clicar em finalizar compra
	browser.find_element_by_xpath("""//*[@id="button-finalize-order-1"]""").click()
	time.sleep(4)

	#selecionar o boleto
	browser.find_element_by_xpath("""//*[@id="boleto"]""").click()
	time.sleep(2)


	#clicar em finalizar compra
	browser.find_element_by_xpath("""/html/body/div/div[2]/form/div[2]/div[4]/div[2]/div/div/button""").click()

	#espera o numero do pedido
	numero_pedido = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH,"""//span[@class="sel-order-nr"]"""))).text

	#pega o horário
	hora = datetime.today()
	#mostra numero do pedido e hora
	pedidos.append((numero_pedido, hora))
	print(numero_pedido, hora, site)



def enviar_email(erro, site):
	#login no meail
	de = servicedesk_email
	para = "dft.servicedesk@dafiti.com.br"
	senha = "Sd2019monitoracao"

	msg = MIMEMultipart()
	msg ['From'] = de
	msg['To'] = para
	msg['Subject'] = "Erro na compra"

	body = "Ocorreu um erro na compra do site [{1}]:\n({0})".format(erro, site)

	# anexa imagem
	image = MIMEImage(open('error.png','rb').read())
	msg.attach(image)
	# anexa o texto
	msg.attach(MIMEText(body, 'plain'))

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(de, senha)
	s.sendmail(de, para, msg.as_string())
	print('mensagem enviada')
	s.quit()


# AQUI COMECA RODAR O CODIGO
if __name__ == "__main__":

	mobile_emulation = {

    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }

	chrome_options = Options()

	chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

	browser = webdriver.Chrome(chrome_options = chrome_options)

	#lista de skus para buscar
	skus = []

	urls = [
	 'https://www.dafiti.com.br/Kit-3pcs-Meias-Lupo-Classic-Preta-2767001.html',
	  'https://www.kanui.com.br/Kit-3pcs-Meias-Lupo-Classic-Preta-2767001.html',
	  'https://www.tricae.com.br/Kit-3pcs-Meias-Lupo-Classic-Preta-2767001.html'
	]

	sites = ['dafiti', 'kanui', 'tricae']

	pedidos = []

	# tente
	try:
		
		for url,site in zip(urls,sites):
			comprar(url, site)
		
		
		
	# exceto erro
	except Exception as erro:
		browser.save_screenshot('error.png')
		enviar_email(erro, site)
		# força o erro e interrupção do script
		raise
	browser.quit()
	