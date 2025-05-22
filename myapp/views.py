import datetime

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myapp.models import *
# Create your views here.

def login(request):
    return render(request,'index.html')

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    ob=loginTbl.objects.filter(username=username,password=password)
    if ob.exists():
        obb=loginTbl.objects.get(username=username,password=password)
        request.session["lid"]=obb.id
        if obb.type =='hospital':
            return HttpResponse('''<script>alert('hospital login successful');window.location='admin_homehosp';</script>''')
        elif obb.type == 'doctor':
            return HttpResponse('''<script>alert('Doctor login successful');window.location='dochome';</script>''')

        else:
            return HttpResponse('''<script>alert('invalid');window.location='/';</script>''')
    else:
        return HttpResponse('''<script>alert('invalid');window.location='/';</script>''')

def admin_add_doctor(request):
    return render(request,'hospital/addnewdoc.html')

def admin_adddoc_post(request):
    name=request.POST["textfield"]
    education=request.POST["textfield2"]
    experience=request.POST["textfield22"]
    PreviousHospital=request.POST["textfield222"]
    phoneno=request.POST["textfield223"]
    email=request.POST["textfield224"]
    certification=request.FILES["file"]
    image=request.FILES["file2"]
    fs=FileSystemStorage()
    fp=fs.save(image.name,image)
    username=request.POST["user"]
    password=request.POST["pass"]

    fs1=FileSystemStorage()
    fp1=fs1.save(certification.name,certification)

    ob=loginTbl()
    ob.username=username
    ob.password=password
    ob.type="doctor"
    ob.save()

    obb=doctorTbl()
    obb.LOGIN=ob
    obb.doctorname=name
    obb.doctoredu=education
    obb.docexp=experience
    obb.prevhosp=PreviousHospital
    obb.docphone=phoneno
    obb.docmail=email
    obb.docimage=fp
    obb.doccertificate=fp1



    obb.save()



    return HttpResponse("<script>alert('Added successfully...');window.location='/admin_doctorlist';</script>")

def admin_complaint(request):
    ob=complaintTbl.objects.all()
    return render(request,'hospital/complaint.html',{"data":ob})

def admin_doctorlist(request):
    ob=doctorTbl.objects.all()
    return render(request,'hospital/doctorlist.html',{'val':ob})

# def admin_homehosp(request):
#     return render(request,'hospital/homehosp.html')


def admin_homehosp(request):
    return render(request,'hospital/index.html')


def admin_managesugg(request):
    ob=suggestionTbl.objects.all()
    return render(request,'hospital/managesugg.html',{"data":ob})

def admin_replysend(request):
    return render(request,'hospital/replysend.html')

def admin_sending(request):
    return HttpResponse("<script>alert('Reply Send!!');window.location='/admin_complaint';</script>")


def admin_addschedule(request):
    return render(request,'hospital/schedule.html')


def admin_addsched_post(request):
    fromtime = request.POST["textfield"]
    totime = request.POST["textfield2"]
    date = request.POST["textfield22"]

    ob=scheduleTbl()
    ob.DOCID_id=request.session["docid"]
    ob.sdate=date
    ob.ftime=fromtime
    ob.ttime=totime
    ob.save()
    return admin_viewscheddoc(request,request.session["docid"])

def admin_updatedsched(request,id):
    request.session["id"]=id
    od=scheduleTbl.objects.get(id=id)
    return render(request,'hospital/updatedsched.html',{'data':od})

def admin_updatesave(request):
    ob=scheduleTbl.objects.get(id=request.session["id"])
    ob.sdate=request.POST["textfield"]
    ob.ftime=request.POST["textfield2"]
    ob.ttime=request.POST["textfield3"]
    ob.save()
    return HttpResponse("<script>alert('Updated');window.location='/admin_viewsheddoc';</script>")


def admin_viewbooking(request):
    ob = bookingTbl.objects.all()
    return render(request,'hospital/viewbooking.html',{"data":ob})

def admin_rejectbooking(request,id):
    ob=bookingTbl.objects.get(id=id)
    op=loginTbl.objects.get(id=ob.LOGIN_id)
    op.type='Rejected'
    op.save()
    return HttpResponse("<script>alert('Approved');window.location='/admin_viewbooking';</script>")


def admin_approvebooking(request,id):
    ob=bookingTbl.objects.get(id=id)
    ob.status='rejected'
    ob.save()
    return HttpResponse("<script>alert('Rejected');window.location='/admin_viewbooking';</script>")

def admin_viewfeed(request):
    ob=feedbackTbl.objects.all()
    return render(request,'hospital/viewfeed.html',{"data":ob})

def admin_viewsheddoc(request):
    ob=scheduleTbl.objects.all()
    return render(request,'hospital/viewscheddoc.html',{"doc":ob})


def adminRejectDoctor(request,id):
    ob=doctorTbl.objects.get(id=id)
    op=loginTbl.objects.get(id=ob.LOGIN_id)
    op.type='Rejected'
    op.save()
    return HttpResponse("<script>alert('Blocked!!');window.location='/admin_doctorlist';</script>")


def adminunblockDoctor(request,id):
    ob=doctorTbl.objects.get(id=id)
    op=loginTbl.objects.get(id=ob.LOGIN_id)
    op.type='doctor'
    op.save()
    return HttpResponse("<script>alert('Unblocked!!');window.location='/admin_doctorlist';</script>")


def admindoctorsearch(request):
    doctor=request.POST["textfield"]
    ob=doctorTbl.objects.filter(doctorname__contains=doctor)
    return render(request,'hospital/doctorlist.html',{'val':ob,'doc':doctor})

def admin_schedsearch(request):
    doctor=request.POST["textfield"]
    ob=scheduleTbl.objects.filter(DOCID__doctorname__contains=doctor)
    return render(request, 'hospital/viewscheddoc.html', {'doc': ob, 'doctor': doctor})


def admin_viewscheddoc(request,id):
    request.session["docid"]=id
    ob=scheduleTbl.objects.filter(DOCID_id=id)
    return render(request,'hospital/viewscheddoc.html',{"doc":ob})

def admin_logout(request):
    return HttpResponse("<script>alert('Logged out');window.location='/';</script>")

#DOCTOR

def dochome(request):
    return render(request,'Doctor/dochome.html')

def doclogout(request):
    return HttpResponse("<script>alert('Logged out');window.location='/';</script>")

def prescription_load(request,id):
    ob=prescription.objects.filter(BOOK=id)
    request.session['pid']=id
    return render(request,'Doctor/prescription.html',{"data":ob})



def addpresc(request):
    return render(request,'Doctor/addpresc.html')

def addpresc_post(request):
    findings=request.POST['textfield2']
    image=request.FILES['file1']
    FS=FileSystemStorage()
    path=FS.save(image.name,image)

    a=prescription()
    a.date=datetime.datetime.now()
    a.findings=findings
    a.prescription=path
    a.BOOK=bookingTbl.objects.get(id=request.session['pid'])
    a.save()
    return HttpResponse("<script>alert('Added');window.location='/viewbooking';</script>")



# def addpresc_post(request):
#     date=request.POST['textfield']
#     findings=request.POST['textfield2']
#     pres=request.FILES['file1']
#     ob=

def updatedoc(request):
    return render(request,'Doctor/updatedoc.html')

def updatepresc(request,id):
    a=prescription.objects.get(id=id)
    return render(request,'Doctor/updatepresc.html',{'data':a})

def updatepresc_post(request):
    id=request.POST['id']
    findings=request.POST['textfield2']

    a=prescription.objects.get(id=id)
    if 'file1' in request.FILES:
        image = request.FILES['file1']
        FS = FileSystemStorage()
        path = FS.save(image.name, image)
        a.prescription = path

    a.date=datetime.datetime.now()
    a.findings=findings
    a.BOOK=bookingTbl.objects.get(id=request.session['pid'])
    a.save()
    return HttpResponse("<script>alert('Updated');window.location='/viewbooking';</script>")



def updatesched(request):
    ob=scheduleTbl.objects.filter(DOCID__LOGIN=request.session["lid"])
    return render(request,'Doctor/updatesched.html',{"data":ob})

def viewbooking(request):
    ob = bookingTbl.objects.filter(SCHEDULE__DOCID__LOGIN=request.session["lid"])
    return render(request,'Doctor/viewbooking.html',{"data":ob})

def viewdetails(request):
    return render(request,'Doctor/viewdetails.html')

def viewProfile(request):
    ob=doctorTbl.objects.get(id=request.session['lid'])
    return render(request,'Doctor/viewProfile.html',{'data':ob})

def updatedetails(request):
    edu= request.POST["textfield"]
    phone=request.POST["textfield2"]

    ob = doctorTbl.objects.get(id=request.session["lid"])

    if 'file' in request.FILES:
        certificate = request.FILES["file"]
        fs=FileSystemStorage()
        fp=fs.save(certificate.name,certificate)


    ob.doctoredu=edu
    ob.docphone=phone
    ob.doccertificate=fp
    ob.save()
    return HttpResponse("<script>alert('Updated');window.location='/viewProfile';</script>")




def android_login(request):
    username=request.POST['username']
    password=request.POST['password']
    ob=loginTbl.objects.filter(username=username,password=password)
    if ob.exists():
        obb=loginTbl.objects.get(username=username,password=password)
        if obb.type =='user':
            return JsonResponse({'status':'ok','lid':str(obb.id),'type':obb.type})

        else:
            return JsonResponse({'status':'not ok'})
    else:
        return JsonResponse({'status': 'not ok'})




def user_reg(request):
    usename=request.POST['usename']
    email=request.POST['email']
    pin=request.POST['pin']
    place=request.POST['place']
    phoneno=request.POST['phoneno']
    password=request.POST['password']

    a=loginTbl()
    a.username=usename
    a.password=password
    a.type='user'
    a.save()

    b=userTbl()
    b.usename=usename
    b.email=email
    b.pin=pin
    b.place=place
    b.phoneno=phoneno
    b.LOGIN=a
    b.save()
    return JsonResponse({'status': 'ok'})


def user_view_doctor(request):
    a=doctorTbl.objects.all()
    l=[]
    for i in a:
        l.append({'id':i.id,'doctorname':i.doctorname,'docexp':i.docexp,'doctoredu':i.doctoredu,'docimage':request.build_absolute_uri(i.docimage.url) if i.docimage else '' })

    print(l)
    return JsonResponse({'status': 'ok','data':l})


def user_view_doctor_schedule(request):
    did=request.POST['did']
    a=scheduleTbl.objects.filter(DOCID_id=did)
    l=[]
    for i in a:
        l.append({'id':i.id,'sdate':str(i.sdate),
                  'ftime':str(i.ftime),
                  'ttime':str(i.ttime),
                  })
    return JsonResponse({'status': 'ok','data':l})

def user_book_doctor(request):
    schedule_id = request.POST['did']
    lid = request.POST['lid']
    ob=bookingTbl()
    ob.bdate=datetime.datetime.now().date()
    ob.status="pending"
    ob.btime=datetime.datetime.now().time()
    ob.SCHEDULE_id=schedule_id
    ob.USERID=userTbl.objects.get(LOGIN=lid)
    ob.save()
    return JsonResponse({'status':'ok'})

def sendfeedback(request):
    lid=request.POST['lid']
    did=request.POST['did']
    feedback=request.POST['feedback']

    a=feedbackTbl()
    a.feedback=feedback
    a.fdate=datetime.datetime.now().today().date()
    a.USERID=userTbl.objects.get(LOGIN_id=lid)
    a.DOC=doctorTbl.objects.get(id=did)
    a.save()
    print("===================================")
    return JsonResponse({'status': 'ok'})

def sendcomplaint(request):
    lid=request.POST['lid']
    complaint=request.POST['complaint']

    a=complaintTbl()
    a.complaint=complaint
    a.cdate=datetime.datetime.now().today().date()
    a.USERID=userTbl.objects.get(LOGIN_id=lid)
    a.save()
    return JsonResponse({'status': 'ok'})

def viewreply(request):
    lid=request.POST['lid']
    ob=complaintTbl.objects.filter(USERID__LOGIN=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'reply':i.reply,'date':str(i.cdate),'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})

def search_doctor(request):
    doctorname=request.POST['doctorname']
    obj = doctorTbl.objects.filter(doctorname__icontains=doctorname)
    mdata = []
    for doctor in obj:
        data = {
            'id':doctor.id,
            'doctorname': doctor.doctorname,
        }
        mdata.append(data)
    return JsonResponse({"status":"ok","data":mdata})

def user_view_booking(request):
    lid = request.POST['lid']
    user = userTbl.objects.get(LOGIN=lid)
    booking = bookingTbl.objects.filter(USERID=user).order_by('-id')
    data = []
    for i in booking:
        data.append({
            'id':i.id,
            'booked_date':i.bdate,
            'status':i.status,
            'btime':i.btime,
            'ftime':i.SCHEDULE.ftime,
            'ttime':i.SCHEDULE.ttime,
            'doctor':i.SCHEDULE.DOCID.doctorname,
            'phone':i.SCHEDULE.DOCID.docphone,
        })
    return JsonResponse({'status':'ok','data':data})

from .predictionfile import  predict
def image_upload(request):
   img=request.FILES['image']

   fs=FileSystemStorage()
   fn=fs.save(img.name,img)
   print(fn)
   res=predict(r"C:\Users\Fatema Hana\PycharmProjects\eyecancer\eyecancer\media/"+fn)
   print(res)
   return JsonResponse({"task":"ok","result":str(res[0]),"fn":"media/"+fn})