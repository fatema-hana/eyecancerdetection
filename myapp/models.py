from django.db import models

# Create your models here.
class loginTbl(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)


class userTbl(models.Model):
    LOGIN=models.ForeignKey(loginTbl,on_delete=models.CASCADE)
    usename=models.CharField(max_length=100)
    email=models.EmailField()
    pin=models.BigIntegerField()
    place=models.CharField(max_length=100)
    phoneno=models.BigIntegerField()


class doctorTbl(models.Model):
    LOGIN=models.ForeignKey(loginTbl,on_delete=models.CASCADE)
    doctorname=models.CharField(max_length=100)
    doctoredu=models.CharField(max_length=200)
    docexp=models.CharField(max_length=200)
    prevhosp=models.CharField(max_length=100)
    docphone=models.BigIntegerField()
    docmail=models.EmailField()
    doccertificate=models.FileField()
    docimage=models.FileField()

class scheduleTbl(models.Model):
    sdate=models.DateField()
    ftime=models.TimeField()
    ttime=models.TimeField()
    DOCID=models.ForeignKey(doctorTbl,on_delete=models.CASCADE)

class feedbackTbl(models.Model):
    feedback=models.CharField(max_length=300)
    fdate=models.DateField()
    USERID = models.ForeignKey(userTbl, on_delete=models.CASCADE)
    DOC=models.ForeignKey(doctorTbl,on_delete=models.CASCADE)

class complaintTbl(models.Model):
    complaint=models.CharField(max_length=500)
    reply=models.CharField(max_length=500,default='pending')
    cdate=models.DateField()
    USERID = models.ForeignKey(userTbl, on_delete=models.CASCADE)

class bookingTbl(models.Model):
    bdate=models.DateField()
    status=models.CharField(max_length=500)
    btime=models.TimeField()
    SCHEDULE=models.ForeignKey(scheduleTbl,on_delete=models.CASCADE)
    USERID = models.ForeignKey(userTbl, on_delete=models.CASCADE)
class suggestionTbl(models.Model):
    suggestion=models.CharField(max_length=500)
    description=models.CharField(max_length=500)
    sugdate=models.DateField()
    USERID = models.ForeignKey(userTbl, on_delete=models.CASCADE)

class prescription(models.Model):
    prescription=models.FileField()
    date = models.DateField()
    findings=models.CharField(max_length=100)
    BOOK=models.ForeignKey(bookingTbl,on_delete=models.CASCADE)



