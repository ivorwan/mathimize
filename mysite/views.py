from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
#from polls.models import Choice, Poll
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.core.mail import send_mail
import random
from mysite.models import Level, Worksheet, ContactForm

# Create your views here.

		
#def detail(request, poll_id):
#    p = get_object_or_404(Poll, pk=poll_id)
#    return render_to_response('polls/detail.html', {'poll': p}, context_instance=RequestContext(request))	



class Terms:
    def __init__(self, term1, term2, operator):
        self.term1 = term1
        self.term2 = term2
        self.operator = operator


class BasicArithmeticForm(forms.Form):		
    rows = forms.IntegerField()
    cols = forms.IntegerField()
    operator = forms.CharField()
	
def basicAddition(request):
    if request.method == 'POST':
        form = BasicArithmeticForm(request.POST)
        if form.is_valid():
            #url = reverse('generatePDF', kwargs={ 'rows': form.cleaned_data["rows"], 'cols': form.cleaned_data["cols"] } )
            url = reverse('generatePDFWorksheet', kwargs={ 'level': 'Level1' } )

            return HttpResponseRedirect(url)
            #return HttpResponseRedirect('some_view2/')
            #return render(request, 'addition/basic.html', {'form':form,})

    else:
        form = BasicArithmeticForm()
        form.operator = "+"
    
    return render(request, 'addition/basic.html', {'form':form,})

#def worksheets(request):
#    p = Worksheet.objects.all()
#    return render_to_response('worksheets.html', {'worksheets' : p}, context_instance = RequestContext(request))

# def some_view(request):
#     # response = HttpResponse(content_type='application/pdf')
#     # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#     # p = canvas.Canvas(response)
#     # p.drawString(100, 100, "Hello World.")
#     # p.showPage()
#     # p.save()
#     # return response
#     return



class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            self.draw_title()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_title(self):
        self.setFont("Helvetica", 8)
        self.drawRightString(7.8 * inch, 10.25 * inch, "Mathimize.com")
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.setFillColorRGB(0.47, 0.47, 0.47)
        self.setFont("Helvetica", 6)

        self.drawRightString(200 * mm, 15 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))




def generatePDFWorksheet(request, worksheet_id):
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="simple_table_grid.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    #Two Columns

    frame_title = Frame(doc.leftMargin, doc.height + 50, doc.width, 25, id='title', showBoundary=0)
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height - 30, id='col1', showBoundary=0)
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height - 30, id='col2', showBoundary=0)

    #frame1.drawBoundary(canvas)
    #frame2.drawBoundary(canvas)

    worksheet = Worksheet.objects.get(pk=worksheet_id)
    worksheet_name = worksheet.get_worksheet_name()

    #termsList = locals().get("Level1")
    worksheetInstance = globals()[worksheet_name]()
    worksheetInstance.number_of_exercises = worksheet.number_of_exercises
    worksheetInstance.level = worksheet.level

    ptext = '<font size=10 color=#F00>%s - Level %s</font>' % (worksheet_name, worksheet.level.level_name)
    elements.append(Paragraph(ptext, styles["Normal"]))

    h1 = ParagraphStyle(name='test', fontSize=10, leading=16, alignment=2, rightIndent=20, fixedWidth=100)


    #termsList = Level1().getTerms()
    termsList = worksheetInstance.getTerms()
    ptext = ""

    data = []
    for t in termsList:
        data.append([t.term1, t.operator, t.term2, '='])
    t = Table(data)
    t.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1), 15),
                           ('BOTTOMPADDING',(0,0),(-1,-1), 9),
                            ('TEXTCOLOR',(0,0),(-1,-1),colors.black)]))
    elements.append(t)
#    for t in termsList:
#        ptext = '<font size=15>%s %s %s = </font>TASD<br/><br/>' % (t.term1, t.operator, t.term2)
#        p = Paragraph(ptext, h1)

        #elements.append(Paragraph(ptext, styles["Normal"]))
#        elements.append(p)



        #elements.append(Spacer(1, 15, isGlue=True))


    doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame_title, frame1,frame2]), ])

    # write the document to disk
    doc.build(elements, canvasmaker=NumberedCanvas)

    return response




#def generatePDF(request, rows, cols):
#    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = 'attachment; filename="simple_table_grid.pdf"'
#
#    # doc = SimpleDocTemplate("simple_table_grid.pdf", pagesize=letter)
#    doc = SimpleDocTemplate(response, pagesize=letter)
#    # container for the 'Flowable' objects
#   elements = []

#   data= [['00', '01', '02', '03', '04'],
#      ['10', '11', '12', '13', '14'],
#      ['20', '21', '22', '23', '24'],
#      ['30', '31', '32', '33', '34']]

#   t=Table(data)
#   t.setStyle(TableStyle([('BACKGROUND',(1,1),(3,2),colors.green),
#                          ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))

#   elements.append(t)

#   styles = getSampleStyleSheet()
#   styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))


#   ptext = '<font size=12>ROWS: %s. <br/> COLS: %s</font>' % (rows, cols)


#   elements.append(Paragraph(ptext, styles["Normal"]))
#   elements.append(Spacer(1, 12))

    # write the document to disk
#   doc.build(elements)
#   return response



class Doubles(Worksheet):
    def getTerms(self):
        termsList = []
        previousTerm = 0
        for i in range(1, self.number_of_exercises):
            term1 = self.getDifferentRandomTerm(previousTerm)
            previousTerm = term1
            t = Terms(term1, term1, "+")
            termsList.append(t)

        return termsList

    def getDifferentRandomTerm(self, term1):
        newTerm = random.randint(1, 9)
        while (newTerm == term1):
            newTerm = random.randint(1, 9)
        return newTerm


class Addition(Worksheet):
    def getTerms(self):
        termsList = []
        for i in range(self.number_of_exercises):
            if self.level.level_name == 'I':
                maxInt = 9
                term1 = random.randint(1, maxInt)
                term2 = self.getDifferentRandomTerm(term1, 1, maxInt )
            if self.level.level_name == 'II':
                maxInt = 99
                term1 = random.randint(10, maxInt)
                term2 = self.getDifferentRandomTerm(term1, 10, maxInt )
            t = Terms(term1, term2, "+")
            termsList.append(t)
        return termsList

    def getDifferentRandomTerm(self, term1, minInt, maxInt):
        newTerm = random.randint(minInt, maxInt)
        while (newTerm == term1):
            newTerm = random.randint(minInt, maxInt)
        return newTerm


def contact(request):
     if request.method == 'POST':

         form = ContactForm(request.POST) # A form bound to the POST data
         if form.is_valid(): # All validation rules pass
             send_mail(form.cleaned_data["subject"], form.cleaned_data["message"], form.cleaned_data["sender"], ['admin@mathimize.com'], fail_silently=False)
             return HttpResponseRedirect('/thankyou/')
     else:
         form = ContactForm()

     return render(request, 'contact.html', { 'form': form, })

