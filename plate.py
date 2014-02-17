import mechanize
import cookielib
import re
import sys
print "California DMV personalized plate availability checker by Kris Linquist (kris@linquist.com)"

if len(sys.argv) < 2:

	print "Usage: python plate.py PLATE1 <PLATE2> <PLATE3> ..."
	print "** Please omit all spaces.  The DMV considers \"HACK THS\" the same plate as HACKTHS"
	sys.exit()


br = mechanize.Browser()
cj = mechanize.CookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
print "Loading DMV page..."

r = br.open('https://www.dmv.ca.gov/ipp2/initPers.do')
html = r.read()

for form in br.forms():
    if form.attrs['id'] == 'PersonalizeFormBean':
        br.form = form
        break
br.form.set_all_readonly(False)
br.form['imageSelected'] = 'platePetLoversPers.jpg'
br.find_control(name="vehicleType").value = ["AUTO"]
br.find_control(name="isVehLeased").value = ["no"]
br.find_control(name="plateType").value = ["R"]
br.submit()

print "Checking plates..."
for plate in sys.argv:
	if (plate.find (".py")) == -1:
		plate = plate.upper()
		platearray = list(plate)
		platearray = platearray + ["*"] * (7 - len(platearray))
		r = br.open('https://www.dmv.ca.gov/wasapp/ipp2/processPers.do')
		for form in br.forms():
		    if form.attrs['id'] == 'PersonalizeFormBean':
		        br.form = form
		        break
		br.form.set_all_readonly(False)
		br.find_control(name="plateChar0").value = [platearray[0]]
		br.find_control(name="plateChar1").value = [platearray[1]]
		br.find_control(name="plateChar2").value = [platearray[2]]
		br.find_control(name="plateChar3").value = [platearray[3]]
		br.find_control(name="plateChar4").value = [platearray[4]]
		br.find_control(name="plateChar5").value = [platearray[5]]
		br.find_control(name="plateChar6").value = [platearray[6]]
		br.submit()
		dmvres = br.response().read()
		if dmvres.find("Sorry, the plate you have requested is not available") == -1:
		    print plate + " is available!"
		else:
		    print plate + " not available"




