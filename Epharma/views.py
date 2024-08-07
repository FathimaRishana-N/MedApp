import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Avg
from django.http import HttpResponse
from django.shortcuts import render

from Epharma.models import *
# ijvk fiyj dnfk uuqg

systempath = r"D:\untitled\Epharma\static\medicine photo\\"

def log(request):
    return render(request,"index.html")

def landingpage(request):
    return render(request,"loginindex.html")


def logpost(request):
    un = request.POST['textfield2']
    p = request.POST['textfield']
    l = login.objects.filter(username=un,password=p)
    if l.exists():
        l = l[0]
        request.session['lid'] = l.id
        request.session['lin'] = "1"
        request.session['h'] = ""
        if l.usertype == 'admin':
            return HttpResponse("<script>alert('Welcome admin home');window.location='/Adminhome'</script>")
        elif l.usertype == 'pharmacy':
            request.session['pid']=pharmacy.objects.get(LOGIN=l.id).id

            return HttpResponse("<script>alert('Welocome home');window.location='/Home'</script>")

        else:
            return HttpResponse("<script>alert('Wait for verification');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('doesnt exist');window.location='/'</script>")


def addmedicine(request):
    request.session['h'] = "ADD MEDICINE"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")
    return render(request,"admin/ADD.html")

def medicinepost(request):
    name = request.POST['textfield']
    Type = request.POST['textfield2']
    if Medicine.objects.filter(name = name).exists():
        return HttpResponse("<script>alert('Already added');window.location='/addmedicine#services'</script>")

    mobj = Medicine()
    mobj.name = name
    mobj.type = Type
    mobj.save()
    return HttpResponse("<script>alert('Added successfully');window.location='/addmedicine#services'</script>")



def feedback(request):
    request.session['h'] = "VIEW FEEDBACK"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data=Feedback.objects.all()
    return render(request,"admin/Feedback.html",{"data":data})

def rating(request,id):
    request.session['h'] = "VIEW RATING"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data=Rating.objects.filter(PHARMACY=id)
    da = []

    for im in data:
        fs = "/static/star/full.jpg"
        hs = "/static/star/half.jpg"
        es = "/static/star/empty.jpg"
        ar = []
        a = float(im.userrating)

        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]


        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]

        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]


        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]


        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]


        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]


        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]


        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]


        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]


        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]


        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]

        da.append({
            'userrating': ar,
            'review': im.review,
            'date': im.date,
            'USER': im.USER,
            'PHARMACY': im.PHARMACY
        })


    return render(request,"admin/Rating.html",{"data":da})


def users(request):
    request.session['h'] = "VIEW USER"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")
    data = user.objects.all()
    return render(request,"admin/user.html",{"data":data})


def viewpharma1(request):
    request.session['h'] = "VIEW PHARMA1"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")
    data = pharmacy.objects.filter(LOGIN__usertype='pharmacy')
    return render(request,"admin/view pharma 1.html",{"data":data})


def viewpharma(request):
    request.session['h'] = "VIEW PHARMA"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")
    data = pharmacy.objects.filter(LOGIN__usertype = 'pending')
    return render(request,"admin/view pharma.html",{"data":data})

def pharmaaccept(request,id,em):
    request.session['h'] = "ACCEPT PHARMACY"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    login.objects.filter(id = id).update(usertype='pharmacy')

    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('epharmacy377@gmail.com', 'ijvk fiyj dnfk uuqg')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    msg = MIMEText("your verification succesfuly completed")

    msg['Subject'] = 'Verification'

    msg['To'] = em

    msg['From'] = 'epharmacy377@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))
    return HttpResponse("<script>alert('accept successfully');window.location='/viewpharma#services'</script>")

def pharmareject(request,id,em):
    request.session['h'] = "REJECT PHARMACY"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    login.objects.get(id = pharmacy.objects.get(id = id).LOGIN.id).delete()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('epharmacy377@gmail.com', 'ijvk fiyj dnfk uuqg')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    msg = MIMEText("your verification rejected")

    msg['Subject'] = 'Verification'

    msg['To'] = em

    msg['From'] = 'epharmacy377@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))
    return HttpResponse("<script>alert('rejected successfully');window.location='/viewpharma#services'</script>")


def view1(request):
    request.session['h'] = "VIEW"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data = Medicine.objects.all()
    return render(request,"admin/view1.html",{"data":data})

def deletemedicine(request,id):
    request.session['h'] = "DELETE MEDICINE"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    Medicine.objects.get(id = id).delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/view1#services'</script>")


def password(request):
    request.session['h'] = "CHANGE PASSWORD"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    return render(request,"admin/password.html")
def passwordpost(request):
    cp=request.POST['textfield']
    chp=request.POST['textfield2']
    np=request.POST['textfield3']
    if login.objects.filter(usertype='admin',password=cp).exists():
        if cp == chp:
            return HttpResponse("<script>alert('same password');window.location='/password'</script>")
        if chp==np:
            login.objects.filter(usertype='admin').update(password=chp)
            return HttpResponse("<script>alert('password changed successfully');window.location='/'</script>")
        else:
            return HttpResponse("<script>alert('password incorrect');window.location='/password'</script>")
    else:
        return HttpResponse("<script>alert('current password incorrect');window.location='/password'</script>")




def Adminhome(request):
    request.session['h'] = "ADMIN HOME"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    return render(request,"admin/index.html")

# ==========================================================================================================================================================================


def Registration(request):
    request.session['h'] = "REGISTRATION"
    return render(request, "pharmacy/Registration.html")
def Registrationpost(request):
    n = request.POST['textfield']
    e = request.POST['textfield3']
    p = request.POST['textfield4']
    la = request.POST['textfield5']
    lo = request.POST['textfield6']
    pas = request.POST['textfield7']
    lobj = login()
    lobj.username = e
    lobj.password=pas
    lobj.usertype = 'pending'
    lobj.save()
    dobj = pharmacy()
    dobj.name = n
    dobj.email = e
    dobj.phone = p
    dobj.latitude = la
    dobj.longitude = lo
    dobj.LOGIN=lobj
    dobj.save()
    return HttpResponse("<script>alert('registered successfully');window.location='/'</script>")

def viewprofile(request):
    request.session['h'] = "PROFILE"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data = pharmacy.objects.get(id = request.session['pid'])
    return render(request,"pharmacy/view profile and update.html",{"data":data})




def profilepost(request):
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    n = request.POST['textfield']
    e = request.POST['textfield2']
    p = request.POST['textfield5']
    la = request.POST['textfield3']
    lo = request.POST['textfield4']
    pharmacy.objects.filter(id =request.session['pid'] ).update(name=n,email=e, phone=p,latitude=la,longitude=lo)
    return HttpResponse("<script>alert('updated successfully');window.location='viewprofile'</script>")



def viewmedicine(request):
    request.session['h'] = "VIEW MEDICINE"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    mid = []
    for i in Medicine.objects.all():
        if stock.objects.filter(Q(PHARMACY=request.session['pid']),MEDICINE=i.id).exists():
            pass
        else:
            mid.append(
                {
                    'id':i.id,
                    'name':i.name,
                    'type':i.type,
                }
            )
    return render(request, "pharmacy/view medicine.html",{"data":mid})


def stockupdate(request,id):
    request.session['h'] = "STOCK UPDATE"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    return render(request, "pharmacy/stock update.html",{"id":id})


def stockupdatepost(request,id):
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    n = request.POST['textfield']
    s = request.POST['textfield2']
    price = request.POST['price']
    f= request.FILES['f']
    d = datetime.now().strftime("%Y%m%d%H%M%S")
    fs = FileSystemStorage()
    fs.save(systempath+d+'.jpg',f)
    sobj = stock()
    sobj.MEDICINE_id = id
    sobj.quantity= n
    sobj.size = s
    sobj.price = price
    sobj.file = '/static/medicine photo/'+d+'.jpg'
    sobj.PHARMACY_id = request.session['pid']
    sobj.save()
    return HttpResponse("<script>alert('stock updated successfully');window.location='/viewstock'</script>")


def viewstock(request):
    request.session['h'] = "VIEW STOCK"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data=stock.objects.filter(PHARMACY=request.session['pid'])
    return render(request, "pharmacy/view stock.html",{"data":data})



def deletestock(request,id):
    request.session['h'] = "DELETE STOCK"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    stock.objects.get(id = id).delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/viewstock'</script>")



def viewbooking(request):
    request.session['h'] = "VIEW BOOKING"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    return render(request, "pharmacy/view booking.html")


def previous(request):
    request.session['h'] = "VIEW PREVIOUS"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data =  purchase.objects.filter(PHARMACY=request.session['pid'],status='approved')
    return render(request, "pharmacy/previous booking.html",{"data":data})


def vieworderitem(request,id):
    request.session['h'] = "VIEW ORDER"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data = purchasehub.objects.filter(PURCHASE=id)
    data2 = []
    for i in data:
        data2.append({
            'id':i.id,
            'STOCK':i.STOCK,
            'quantity':i.quantity,
            'PURCHASE':i.PURCHASE,
            'price': int(i.quantity) * int(i.STOCK.price),

        })
    return render(request, "pharmacy/view order item.html",{"data":data2})


def verify(request):
    request.session['h'] = "VERIFY"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data = purchase.objects.filter(PHARMACY=request.session['pid'],status='pending')
    return render(request, "pharmacy/verify.html",{"data":data})



def vaccept(request,id):
    request.session['h'] = "ACCEPT"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    purchase.objects.filter(id = id).update(status='approved')
    return HttpResponse("<script>alert('approved successfully');window.location='/verify'</script>")


def vreject(request,id):
    request.session['h'] = "REJECT"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    purchase.objects.filter(id = id).update(status='rejected')
    return HttpResponse("<script>alert('rejected');window.location='/verify'</script>")




def phrating(request):
    request.session['h'] = "PHARMACY RATING"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data = Rating.objects.filter(PHARMACY= request.session['pid'])
    da = []

    for im in data:
        fs = "/static/star/full.jpg"
        hs = "/static/star/half.jpg"
        es = "/static/star/empty.jpg"
        ar = []
        a = float(im.userrating)

        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]
            

        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]
           
        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]
            

        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]
            

        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]
            

        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]
            

        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]
            

        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]
            

        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]
            

        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]
            

        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]

        da.append({
            'userrating':ar,
            'review':im.review,
            'date':im.date,
            'USER':im.USER,
            'PHARMACY':im.PHARMACY
        })
            
    return render(request, "pharmacy/Rating.html",{"data":da})


def phchangepass(request):
    request.session['h'] = "CHANGE PASSWORD"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    return render(request, "pharmacy/password.html")


def phchangepasspost(request):
    cp=request.POST['textfield']
    chp=request.POST['textfield2']
    np=request.POST['textfield3']
    if login.objects.filter(usertype='pharmacy',password=cp,id = request.session['lid']).exists():
        if cp == chp:
            return HttpResponse("<script>alert('same password');window.location='/phchangepass'</script>")
        if chp==np:

            login.objects.filter(usertype='pharmacy',id= request.session['lid']).update(password=chp)
            return HttpResponse("<script>alert('password changed successfully');window.location='/'</script>")
        else:
            return HttpResponse("<script>alert('password incorrect');window.location='/phchangepass'</script>")
    else:
        return HttpResponse("<script>alert('current password incorrect');window.location='/phchangepass'</script>")


def Home(request):
    request.session['h'] = "HOME"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    return render(request, "pharmacy/Home.html")



def stockupdate2(request,id):
    request.session['h'] = "STOCK UPDATE"
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    data = stock.objects.get(id = id)
    return render(request, "pharmacy/stock update2.html",{"id":id,"data":data})

def stockupdate2post(request,id):
    if request.session['lin'] == '0':
        return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

    q = request.POST['textfield']
    s = request.POST['textfield2']
    price = request.POST['price']

    if 'f' in request.FILES:
        f = request.FILES['f']
        d = datetime.now().strftime("%Y%m%d%H%M%S")
        fs = FileSystemStorage()
        fs.save(systempath + d + '.jpg', f)
        file = '/static/medicine photo/' + d + '.jpg'
        stock.objects.filter(id=id).update(file=file)
    stock.objects.filter(id=id).update(size=s,quantity=q,price=price)
    return HttpResponse("<script>alert('stock updated successfully');window.location='/viewstock'</script>")



def logout(request):
    request.session['h'] = "LOGOUT"
    request.session['lin'] = "0"
    return HttpResponse("<script>alert('Your session has expired');window.location='/'</script>")

