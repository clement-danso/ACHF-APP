from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from smsapp.models import *
from smsapp.forms import *
import requests
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.db.models import Q
from openpyxl import Workbook
import pandas as pd
import io  # Add this line to import the 'io' module
from django.urls import resolve

from datetime import datetime, date, time, timedelta
from django.utils import timezone
import os
import time

# Create your views here.
#

def record_create(request):
    form = RecordsForm()
    context = {'form': form}
    html_form = render_to_string('smsapp/partial_record_create.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})


@login_required
def load_grades(request):
    category_id = request.GET.get('category_id')
    grades = grade.objects.filter(category_id=category_id).order_by('grade')
    
    return render(request, 'smsapp/grades_dropdown_list_options.html', {'grades': grades})


@login_required
def validate_empnumber(request):
    EmpNumber = request.GET.get('EmpNumber')
    data = {
        'is_taken': records.objects.filter(EmpNumber__iexact=EmpNumber).exists()
    }
    print(data)
    return JsonResponse(data)


def records_update(request):
    EmpNumber = request.GET.get('EmpNumber')
    recod = records.objects.filter(Empnumber__iexact=Empnumber)
    
    return JsonResponse(recod)


@login_required
def home(request):
	today = timezone.now().date()
	alrecods=records.objects.all()
	recods=records.objects.all().order_by('-date_created')[:5][::-1]
	deliveries=delivery.objects.all().order_by('-date_created')[:5]
	aldeliveries=delivery.objects.all()
	act_recods=records.objects.filter(status='Active')
	inact_recods=records.objects.filter(status='Inactive')
	
	bdaysms=delivery.objects.filter(smstype='Birthday').count()
	annisms=delivery.objects.filter(smstype='Anniversary').count()
	bsms=delivery.objects.filter(smstype='Broadcast').count()
	welsms=delivery.objects.filter(smstype='Welcome').count()
	
	recodsnum=alrecods.count()
	activenum=act_recods.count()
	inactivenum=inact_recods.count()
	
	context={
		'recods':recods,
		'recodsnum':recodsnum,
		'activenum':activenum, 
		'inactivenum':inactivenum, 
		'deliveries':deliveries,
		'aldeliveries':aldeliveries,
		'alrecods':alrecods,
		'bdaysms': bdaysms,
		'annisms': annisms,
		'bsms': bsms,
		'welsms': welsms,
		} 
	return render(request, 'smsapp/dashboard.html', context)


@login_required
def createrecord(request):
	"""form page for creating records"""

	fm = RecordsForm()
	if request.method == 'POST':
		fm = RecordsForm(request.POST)
		
		if fm.is_valid():
			fm.save()
			messages.success(request, "Record successfully created!")

			fon=request.POST.get('Mobile')
			titlename=request.POST.get('Title')
			firstname=request.POST.get('FirstName')
			lastname=request.POST.get('LastName')
			emaill=request.POST.get('OfficialEmail')
			dateOB=request.POST.get('DOB')
			
			
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			data = {
				'recipient[]': fon,
				'sender': 'HR WNRHD',
				'message': 'Dear %s, You are welcome to the Western North Regional Health Directorate SMS platform. Thank you for joining this great health family.\n\nRSVP: 0204912857' % firstname,
				'is_schedule': False,
				'schedule_date': ''
				}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			
			bstatus=json.dumps(data['status'])
			bsmstype='Welcome'
			btotalsent=json.dumps(data["summary"]["total_sent"])
			btotalrejected=json.dumps(data["summary"]["total_rejected"])
			brecipient=json.dumps(data["summary"]["numbers_sent"])
			bcreditused=json.dumps(data["summary"]["credit_used"])
			bcreditleft=json.dumps(data["summary"]["credit_left"])
			
			delivery_instance = delivery(
										sms_status=bstatus, 
										smstype=bsmstype, 
										total_sent=btotalsent, 
										total_rejected=btotalrejected, 
										recipient=brecipient, 
										credit_used=bcreditused, 
										credit_left=bcreditleft
										)
			delivery_instance.save()
			return redirect('/home')
		
	context = {'fm':fm}
	
	return render(request, 'smsapp/recordfrm.html', context)

def updaterecord(request, pk):
	"""form page for creating orders"""
	record = records.objects.get(EmpNumber=pk)
	fm = RecordsForm(instance=record)
	
	if request.method == 'POST':
		fm = RecordsForm(request.POST or None, instance=record)
		if fm.is_valid():
			fm.save()
			messages.success(request, "Record successfully updated!")
			return redirect('/recordlist')
	else:
		fm = RecordsForm(instance=record)
	
	context = {'fm':fm}
	return render (request, 'smsapp/recordupdatefrm.html', context)


@login_required
def creategroup(request):
	
	fm = GroupForm()
	if request.method == 'POST':
		fm = GroupForm(request.POST)
		
		if fm.is_valid():
			fm.save()
		
		
		return redirect('/grouplist')

	context = {'fm':fm}
	return render(request, 'smsapp/groupfrm.html', context)


@login_required
def bcriteria(request):
	#loaded to the html page
	districts = district.objects.all()
	regions = region.objects.all()
	projects = project.objects.all()
	
	
	#data values from the html page
	crit=request.POST.get('criteria')	
	
	if request.method == 'POST' and crit=='1':
		proj=request.POST.get('project')
		projname=project.objects.get(id=proj).projectName
		filtercriteria='project'
		
		request.session['data'] = filtercriteria, projname
		return redirect('/newbmessagecat')
		
	elif request.method =='POST' and crit=='2':
		minage=request.POST.get('minage')
		maxage=request.POST.get('maxage')
		
		request.session['data'] = [minage, maxage]
		
		return redirect('/newbmessagecat', minage=minage, maxage=maxage)
		
	elif request.method =='POST' and crit=='3':
		reg=request.POST.get('region')
		regname=region.objects.get(id=reg).regionName
		
		request.session['data'] = regname
		
		return redirect('/newbmessagecat')
		
	elif request.method =='POST' and crit=='4':
		dis=request.POST.get('district')
		distname=district.objects.get(id=dis).districtName
				
		request.session['data'] = distname
		
		return redirect('/newbmessagecat')
		
	elif request.method =='POST' and crit=='5':
		status1=request.POST.get('yesno')
		
		request.session['data'] = status1
		
		return redirect('/newbmessagecat')
		
	elif request.method =='POST' and crit=='6':
		status2=request.POST.get('yesno1')
		
		request.session['data'] = status2
		
		return redirect('/newbmessagecat')
		
	elif request.method =='POST' and crit=='7':
		status3=request.POST.get('yesno2')
		
		request.session['data'] = status3
		
		return redirect('/newbmessagecat')
	
	
	elif request.method =='POST' and crit=='8':
		
		return redirect('/newbmessagecat')
	
	
		
	context = {
		'districts':districts,
		'projects':projects,
		'regions':regions
			}
	return render(request, 'smsapp/bcriteria.html', context)

@login_required
def vcriteria(request):
	#loaded to the html page
	districts = district.objects.all()
	regions = region.objects.all()
	projects = project.objects.all()
	
	
	#data values from the html page
	crit=request.POST.get('criteria')	
	
	if request.method == 'POST' and crit=='1':
		proj=request.POST.get('project')
		projname=project.objects.get(id=proj).projectName
		filtercriteria='project'
		
		request.session['data'] = filtercriteria, projname
		return redirect('/newvoicebroadcast')
		
	elif request.method =='POST' and crit=='2':
		minage=request.POST.get('minage')
		maxage=request.POST.get('maxage')
		
		request.session['data'] = [minage, maxage]
		
		return redirect('/newvoicebroadcast', minage=minage, maxage=maxage)
		
	elif request.method =='POST' and crit=='3':
		reg=request.POST.get('region')
		regname=region.objects.get(id=reg).regionName
		
		request.session['data'] = regname
		
		return redirect('/newvoicebroadcast')
		
	elif request.method =='POST' and crit=='4':
		dis=request.POST.get('district')
		distname=district.objects.get(id=dis).districtName
				
		request.session['data'] = distname
		
		return redirect('/newvoicebroadcast')
		
	elif request.method =='POST' and crit=='5':
		status1=request.POST.get('yesno')
		
		request.session['data'] = status1
		
		return redirect('/newvoicebroadcast')
		
	elif request.method =='POST' and crit=='6':
		status2=request.POST.get('yesno1')
		
		request.session['data'] = status2
		
		return redirect('/newvoicebroadcast')
		
	elif request.method =='POST' and crit=='7':
		status3=request.POST.get('yesno2')
		
		request.session['data'] = status3
		
		return redirect('/newvoicebroadcast')
	
	
	elif request.method =='POST' and crit=='8':
		
		return redirect('/newvoicebroadcast')
	
	
		
	context = {
		'districts':districts,
		'projects':projects,
		'regions':regions
			}
	return render(request, 'smsapp/vcriteria.html', context)



@login_required
def createvoicebroad(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	credentials_file = os.path.join(BASE_DIR, 'smsapp/credentials.json')
	
	themes=theme.objects.all()
	audios=AudioFile.objects.all()
	categories=category.objects.all()
	
	received_data = request.session.get('data')
	filtercriteria = received_data[0]
	searchtext= received_data[1]
	print(filtercriteria, searchtext)
	"""form page for creating records"""
	fm = BroadcastmessagecatForm()
	
	if request.method == 'POST':
		fm = BroadcastmessagecatForm(request.POST)
				
				#Broadcast details
		messages.info(request, "Please wait as broadcast details are being saved.....", extra_tags='saving')

		vf_id =request.POST.get('audioid')
		theme_id =request.POST.get('themeid')
		cat_id =request.POST.get('catid')
		
		vf_name= AudioFile.objects.get(id=vf_id).file
		catname=category.objects.get(id=cat_id).catName
		themename=theme.objects.get(id=theme_id).theme
		
		VOICEFILE_path = os.path.join(BASE_DIR, f'media/{vf_name}')
		print(VOICEFILE_path)
		
		
		messages.info(request, "Broadcast details saved!", extra_tags='saved')

				#Individual message
		#Set up credentials	
		messages.info(request, "Authenticating user credentials....", extra_tags='authenticating')
		scope = [
		'https://spreadsheets.google.com/feeds',
		'https://www.googleapis.com/auth/drive'
		]
		credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
		#authenticate client
		client = gspread.authorize(credentials)
		messages.info(request, "Authenticated!", extra_tags='authenticated')
		# Open the Google Sheet by its title or URL
		sheet = client.open('ODK Phone contacts').sheet1
		
		messages.info(request, "Retrieving records based on selected criteria....", extra_tags='retrieving')
		# Retrieve the records by criteria
		gdata = sheet.get_all_records()
		print(gdata)
		
		filtered_data=[record for record in gdata if record[filtercriteria] == searchtext]

		print(filtered_data)
		
		
		#messages.info(request, "Sending broad cast to 1000 entities. This may be a good time to grab some coffee......", extra_tags='sending')
		#messages.get_messages(request).used_tags.clear()

		for recod in gdata:
			print(recod)
			fone=recod['phone']
			ffone=f"0{fone}"
			print(ffone)
			endPoint = 'https://api.mnotify.com/api/voice/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			files = {'file': open(VOICEFILE_path, 'rb')}
			print(files)
			payload = {
			   'campaign': 'First',
			   'recipient[]': ffone,
			   #'files': files,
			   'voice_id': '',
			   'is_schedule': False,
			   'schedule_date': ''
			}
		#	print(data)
			url = endPoint + '?key=' + apiKey
			response = requests.request("POST",url, data=payload, files=files)
			print(response.status_code)
			#data = response.json()
				
			data = json.loads(response.text)
			message_code=(data["code"])
			print(message_code)
			print(data)
			if response.status_code == 200 and message_code == '2000':
				#returns from api call to mnotify
				bstatus=data["status"]
				bsmstype='Voice Broadcast'
				btotalsent=data["summary"]["total_sent"]
				btotalrejected=data["summary"]["total_rejected"]
				brecipient=data["summary"]["numbers_sent"][0]
				bcreditused=data["summary"]["credit_used"]
				bcreditleft=''
				bid=data["summary"]["_id"]
				print(bid)
				
				reportendPoint = 'https://api.mnotify.com/api/call-status/' + bid
				print(reportendPoint)
				reporturl=reportendPoint + '?key=' + apiKey
				time.sleep(3)
				response=requests.get(url)
				data = response.json
				print(data)
				#returns from gsheet
				name=recod['fname']
				age=recod['age']
				gender=recod['gender']
				project=recod['project']
				region=recod['region']
				district=recod['district']
				pregnancy=recod['pregnancy']
				caregiver=recod['caregiver']
				lactating=recod['lactating']
				
				
				
				delivery_instance = delivery(
										call_id=bid,
										sms_status=bstatus, 
										smstype=bsmstype, 
										total_sent=btotalsent, 
										total_rejected=btotalrejected,
										recipient=brecipient, 
										credit_used=bcreditused, 
										credit_left=bcreditleft,
										catname=catname,
										name=name,
										age=int(age) if age else None,
										gender=gender,
										project=project,
										region=region,
										district=district,
										pregnancy_status=pregnancy,
										caregiver=caregiver,
										lactating=lactating,
										)
				delivery_instance.save()
				
				
				
			else:
				estatus=data["status"],
				ecode=data["code"],
				emessage=data["message"],
				name=recod['fname']
				bsmstype='Voice Broadcast'
				brecipient=recod['phone']
				
				
				log_entry = ResponseLog.objects.create(
					status=estatus,
					code=ecode,
					message=emessage,
					smstype='Voice Broadcast',
					recipient=brecipient,
					name=name
					
					
					)
											
		return redirect('/home')
	
	context = {
	'fm':fm,
	'themes':themes,
	'audios':audios,
	'categories':categories
	
	}
	
	return render(request, 'smsapp/bcvoice.html', context)

@login_required
def createbmessagecat(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	credentials_file = os.path.join(BASE_DIR, 'smsapp/credentials.json')
	
	received_data = request.session.get('data')
	filtercriteria = received_data[0]
	searchtext= received_data[1]
	print(filtercriteria, searchtext)
	"""form page for creating records"""
	fm = BroadcastmessagecatForm()
	
	current_url = request.path
	print(current_url)
	if request.method == 'POST':
		fm = BroadcastmessagecatForm(request.POST)
				
				#Broadcast details
		messages.info(request, "Please wait as broadcast details are being saved.....", extra_tags='saving')

		theme_id=request.POST.get('theme')
		themename=theme.objects.get(id=theme_id).theme
		cat=request.POST.get('category')
		catname=category.objects.get(id=cat).catName
		cont=request.POST.get('Content')
		
		
		messages.info(request, "Broadcast details saved!", extra_tags='saved')

				#Individual message
		#Set up credentials	
		messages.info(request, "Authenticating user credentials....", extra_tags='authenticating')
		scope = [
		'https://spreadsheets.google.com/feeds',
		'https://www.googleapis.com/auth/drive'
		]
		credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
		#authenticate client
		client = gspread.authorize(credentials)
		messages.info(request, "Authenticated!", extra_tags='authenticated')
		# Open the Google Sheet by its title or URL
		sheet = client.open('ODK Phone contacts').sheet1
		
		messages.info(request, "Retrieving records based on selected criteria....", extra_tags='retrieving')
		# Retrieve the records by criteria
		gdata = sheet.get_all_records()
		print(gdata)
		
		filtered_data=[record for record in gdata if record[filtercriteria] == searchtext]
		
		
		#messages.info(request, "Sending broad cast to 1000 entities. This may be a good time to grab some coffee......", extra_tags='sending')
		#messages.get_messages(request).used_tags.clear()

		for recod in gdata:
			fone=recod['phone']
			ffone=ffone=f"0{fone}"
			print(recod['phone'])
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			data = {
			   'recipient[]': ffone,
			   'sender': 'HR WNRHD',
			   'message': cont,
			   'is_schedule': False,
			   'schedule_date': ''
			}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			print(data)
			#returns from api call to mnotify
			bstatus=json.dumps(data['status'])
			bstatus=bstatus.replace('"', '')
			bsmstype='SMS Broadcast'
			btotalsent=json.dumps(data["summary"]["total_sent"])
			btotalrejected=json.dumps(data["summary"]["total_rejected"])
			brecipient=json.dumps(data["summary"]["numbers_sent"][0])
			brecipient=brecipient.replace('"', '').replace('"', '')
			bcreditused=json.dumps(data["summary"]["credit_used"])
			bcreditleft=json.dumps(data["summary"]["credit_left"])
			
			#returns from gsheet
			name=recod['fname']
			age=recod['age']
			gender=recod['gender']
			project=recod['project']
			region=recod['region']
			district=recod['district']
			pregnancy=recod['pregnancy']
			caregiver=recod['caregiver']
			lactating=recod['lactating']
			
			
			delivery_instance = delivery(
									sms_status=bstatus, 
									smstype=bsmstype, 
									total_sent=btotalsent, 
									total_rejected=btotalrejected,
									recipient=brecipient, 
									credit_used=bcreditused, 
									credit_left=bcreditleft,
									catname=catname,
									name=name,
									age=age,
									gender=gender,
									project=project,
									region=region,
									district=district,
									pregnancy_status=pregnancy,
									caregiver=caregiver,
									lactating=lactating,
									)
			delivery_instance.save()
						
			return redirect('/home')
	
	context = {'fm':fm}
	
	return render(request, 'smsapp/bcmessagecatfrm.html', context)


@login_required
def createbmessageall(request):
	"""form page for creating records"""
	alrecods=records.objects.all()
	recodsnum=alrecods.count()
	
	
	fm = BroadcastmessageallForm()
	if request.method == 'POST':
		fm = BroadcastmessageallForm(request.POST)
		cat=request.POST.get('category')
		
		br_records= alrecods
		
		cont=request.POST.get('Content')
		
		for recod in br_records:
			fone=[recod.Mobile]
			ffone=f"0{fone}"
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			data = {
			   'recipient[]': ffone,
			   'sender': 'HR WNRHD',
			   'message': cont,
			   'is_schedule': False,
			   'schedule_date': ''
			}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			
			bstatus=json.dumps(data['status'])
			bsmstype='Broadcast'
			btotalsent=json.dumps(data["summary"]["total_sent"])
			btotalrejected=json.dumps(data["summary"]["total_rejected"])
			brecipient=json.dumps(data["summary"]["numbers_sent"])
			bcreditused=json.dumps(data["summary"]["credit_used"])
			bcreditleft=json.dumps(data["summary"]["credit_left"])
			
			delivery_instance = delivery(
									sms_status=bstatus, 
									smstype=bsmstype, 
									total_sent=btotalsent, 
									total_rejected=btotalrejected, 
									recipient=brecipient, 
									credit_used=bcreditused, 
									credit_left=bcreditleft
									)
			delivery_instance.save()
			
			return redirect('/home')
	
	context = {'fm':fm, 'recodsnum':recodsnum}
	
	return render(request, 'smsapp/bcmessageallfrm.html', context)



@login_required
def messtemp(request):
	fm=MesstempForm()
	if request.method == 'POST':
		fm = MesstempForm(request.POST)
		
		
		tit=request.POST.get('Title')
		cont=request.POST.get('Content')
		
		endPoint = 'https://api.mnotify.com/api/template'
		apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
		data = {
		   'title': tit,
		   'content': cont
		}
		url = endPoint + '?key=' + apiKey
		response = requests.post(url, data)
		data = response.json()
		
		messtemp_id=json.dumps(data["_id"])
		messtemp_instance = messagetemp(Template_id=messtemp_id, Title=tit, Content=cont)
		messtemp_instance.save()
		
		return redirect('/home')
	
	context = {'fm':fm}

	return render(request, 'smsapp/messtempfrm.html', context)




@login_required
def audiolist(request):
	audios=AudioFile.objects.all()

	
	context={'audios':audios}
	return render(request, 'smsapp/audiolist.html', context)
	
	
	
#def play_audio(request):
    #audio_file_path = '/path/to/audio/file.mp3'  # Replace with the actual path to your audio file
    
    #response = FileResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')
    #return response

@login_required
def grouplist(request):
	grps=group.objects.all()
	
	context={'grps':grps}
	return render(request, 'smsapp/groups.html', context)

@login_required	
def templatelist(request):
	temps=messagetemp.objects.all()
	
	context={'temps':temps}
	return render(request, 'smsapp/templates.html', context)


@login_required
def deliverylist(request):
	search_term_project = request.GET.get('projectsearch', '')
	search_term_gender = request.GET.get('gendersearch', '')
	search_term_lactating = request.GET.get('lactatingtsearch', '')
	search_term_pregnancy = request.GET.get('pregnancytsearch', '')
	search_term_region = request.GET.get('regionsearch', '')
	search_term_district = request.GET.get('districtsearch', '')
	start_date = request.GET.get('start_date', None)
	end_date = request.GET.get('end_date', None)

	delivs=delivery.objects.all()
	
	distinct_project_values = delivery.objects.values_list('project', flat=True).distinct()
	distinct_region_values = delivery.objects.values_list('region', flat=True).distinct()
	distinct_district_values = delivery.objects.values_list('district', flat=True).distinct()
	distinct_gender_values = delivery.objects.values_list('gender', flat=True).distinct()
	
	if search_term_project:
		delivs = delivs.filter(Q(name__icontains=search_term_project))  # Perform case-insensitive search on field1
	if search_term_gender:
			delivs = delivs.filter(Q(name__icontains=search_term_gender))  # Perform case-insensitive search on field1
	if search_term_lactating:
		delivs = delivs.filter(Q(name__icontains=search_term_lactating))  # Perform case-insensitive search on field1
	if search_term_pregnancy:
		delivs = delivs.filter(Q(name__icontains=search_term_pregnancy))  # Perform case-insensitive search on field1
	if search_term_region:
		delivs = delivs.filter(Q(name__icontains=search_term_region))  # Perform case-insensitive search on field1
	if search_term_district:
		delivs = delivs.filter(Q(name__icontains=search_term_district))
	if start_date and end_date:
		# Convert start_date and end_date to datetime.date objects
		start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
		end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
		end_date = end_date + timedelta(days=1)
		delivs = delivs.filter(date_created__range=[start_date, end_date])

	
	base_download_url='/download/'
	
	# Get the resolved URL for the current request
	resolved_url = request.path
	# Process the resolved URL to obtain the base URL (without parameters)
	base_url = resolved_url.split('?')[0]
	print(base_url)
	#if request.META.get('HTTP_REFERER') == download_url:
	if base_url == base_download_url:
		if not delivs.exists():
			messages.info(request, "Query is empty")
		else:
			# Convert the data to a pandas DataFrame
			df = pd.DataFrame(list(delivs.values()))
			print(delivs)
			# Convert datetime columns to timezone-unaware
			df['date_created'] = df['date_created'].dt.tz_localize(None)

			# Create an Excel file in memory
			excel_file = io.BytesIO()
			writer = pd.ExcelWriter(excel_file, engine='openpyxl')
			df.to_excel(writer, index=False, sheet_name='Sheet1')
			writer.close()
			excel_file.seek(0)

			# Set the appropriate response headers for Excel download
			response = HttpResponse(excel_file.read(),
									content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
			response['Content-Disposition'] = 'attachment; filename=report.xlsx'

			return response	
	
	
	context={
	'delivs':delivs,
	'search_term_project':search_term_project,
	'search_term_gender': search_term_gender,
	'search_term_lactating':search_term_lactating,
	'search_term_pregnancy':search_term_pregnancy,
	'search_term_region':search_term_region,
	'search_term_district':search_term_district,
	'distinct_project_values':distinct_project_values,
	'distinct_region_values': distinct_region_values,
	'distinct_district_values': distinct_district_values,
	'distinct_gender_values':distinct_gender_values,
	
	}
	return render(request, 'smsapp/deliveries.html', context)
#######
@login_required
def responselog(request):
	logs=ResponseLog.objects.all()
	
	if not logs.exists():
		messages.info(request, "Query is empty")
	
	context={
	'logs':logs,
	}
	return render(request, 'smsapp/responselog.html', context)




#######

def update_delivery_records(request):
    # Get all Delivery records that meet the criteria
    records_to_update = delivery.objects.filter(call_id__isnull=False,  answer_time__isnull=True, hang_up_time__isnull=True, answer_period__isnull=True)
    print(records_to_update)
    # Iterate through the records and update them
    for record in records_to_update:
        # Make an API call to retrieve data
        print(record.call_id)
        vc_id=record.call_id
        endpoint ='https://api.mnotify.com/api/call-status/' + vc_id
        api_key = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
        url = endpoint + '?key=' + api_key
        print(url)
        try:
            response = requests.get(url)
            print(response)
            
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)
                    if data.get("status") == "success" and "call" in data:
                        call_data = data["call"]
                        answer_time = call_data.get("answer_time")
                        hang_up_time = call_data.get("hang_up_time")
                        if answer_time and hang_up_time:
                            # Update the Delivery record with the retrieved data
                            record.answer_time = answer_time
                            record.hang_up_time = hang_up_time
                            
                            # Calculate the difference between answer_time and hang_up_time
                            answer_time_obj = datetime.strptime(answer_time, '%Y-%m-%d %H:%M:%S')
                            hang_up_time_obj = datetime.strptime(hang_up_time, '%Y-%m-%d %H:%M:%S')
                            answer_period = hang_up_time_obj - answer_time_obj
                            
                            record.answer_period = answer_period.total_seconds()
                            
                            record.save()
                except json.JSONDecodeError as e:
                    # Handle JSON parsing error
                    print("JSON Parsing Error:", str(e))
                    data = {}
            else:
                # Handle non-200 status codes here
                print("Non-200 Status Code:", response.status_code)
                data = {}
        except requests.exceptions.RequestException as e:
            # Handle API request errors here
            return JsonResponse({"error": str(e)})
        
        print(data)

    return JsonResponse({"message": "Records updated successfully"})


@login_required
def trying(request):
	recods=records.objects.all()
	#record = records.objects.get(EmpNumber=pk)
	fm = RecordsForm()
	
	context={'recods':recods, 'fm':fm}
	return render(request, 'smsapp/students_rv.ejs', context)	
	
	
@login_required
def upload_audio(request):
	fm = AudioFileForm()
	if request.method == 'POST':
		form = AudioFileForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, "Audio successfully uploaded!")
			return redirect('/recordlist')
	else:
		form = AudioFileForm()
	
	context = {'fm':fm}
	return render(request, 'smsapp/upload.html', {'form': form})
	
