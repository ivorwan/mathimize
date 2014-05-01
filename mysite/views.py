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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, BaseDocTemplate, Frame, \
    PageTemplate, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Line

from django.core.mail import send_mail
import random
import sendgrid
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
            url = reverse('generatePDFWorksheet', kwargs={'level': 'Level1'})

            return HttpResponseRedirect(url)
            #return HttpResponseRedirect('some_view2/')
            #return render(request, 'addition/basic.html', {'form':form,})

    else:
        form = BasicArithmeticForm()
        form.operator = "+"

    return render(request, 'addition/basic.html', {'form': form, })


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


class Test:
    def get_worksheet_name(self):
        return self._worksheet_name

    def set_worksheet_name(self, worksheet_name):
        self._worksheet_name = worksheet_name

    worksheet_name = property(get_worksheet_name, set_worksheet_name)


class NumberedCanvas(canvas.Canvas):
    def get_worksheet_name(self):
        return self._worksheet_name

    def set_worksheet_name(self, worksheet_name):
        self._worksheet_name = worksheet_name

    worksheet_name = property(get_worksheet_name, set_worksheet_name)

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
        self.drawRightString(1.75 * inch, 10.25 * inch, self.worksheet_name)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.setFillColorRGB(0.47, 0.47, 0.47)
        self.setFont("Helvetica", 6)

        self.drawRightString(200 * mm, 15 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))


def getDocTemplate(response, pdfLayout):
    #doc = SimpleDocTemplate(response, pagesize=letter)
    doc = BaseDocTemplate(response, pagesize=letter)

    if pdfLayout == 'TWO_COLUMNS':
        #Two Columns
        frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width / 2 - 6, doc.height, id='col1', showBoundary=0)
        frame2 = Frame(doc.leftMargin + doc.width / 2 + 6, doc.bottomMargin, doc.width / 2 - 6, doc.height, id='col2',
                       showBoundary=0)
        doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2]), ])

    if pdfLayout == 'THREE_COLUMNS':
        #Three Columns
        frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width / 3 - 6, doc.height, id='col1', showBoundary=0)
        frame2 = Frame(doc.leftMargin + doc.width / 3 + 6, doc.bottomMargin, doc.width / 3 - 6, doc.height, id='col2',
                       showBoundary=0)
        frame3 = Frame(doc.leftMargin + 2 * doc.width / 3 + 6, doc.bottomMargin, doc.width / 3 - 6, doc.height,
                       id='col3', showBoundary=0)
        doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2, frame3]), ])

    if pdfLayout == 'FOUR_COLUMNS':
        #4 Columns
        frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width / 4 - 6, doc.height, id='col1', showBoundary=0)
        frame2 = Frame(doc.leftMargin + doc.width / 4 + 6, doc.bottomMargin, doc.width / 4 - 6, doc.height, id='col2',
                       showBoundary=0)
        frame3 = Frame(doc.leftMargin + 2 * doc.width / 4 + 6, doc.bottomMargin, doc.width / 4 - 6, doc.height,
                       id='col3', showBoundary=0)
        frame4 = Frame(doc.leftMargin + 3 * doc.width / 4 + 6, doc.bottomMargin, doc.width / 4 - 6, doc.height,
                       id='col4', showBoundary=0)
        doc.addPageTemplates([PageTemplate(id='TwoCol', frames=[frame1, frame2, frame3, frame4]), ])

    return doc


def getFormattedElements(termsList, operationLayout):
    elements = []
    if operationLayout == 'SINGLE_LINE':
        for t in termsList:
            data = []
            data.append([t.term1, t.operator, t.term2, '='])
            tbl = Table(data)
            tbl.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 15),
                                     ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
            elements.append(tbl)
    if operationLayout == 'MULTIPLE_LINES':
        for t in termsList:
            data = []
            data.append(['', t.term1])
            data.append([t.operator, t.term2])

            tbl = Table(data)
            tbl.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 15),
                                     ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)]))
            elements.append(tbl)

            line = MCLine(50)
            elements.append(line)
            elements.append(Spacer(100, 23, isGlue=True))

    return elements


def generatePDFWorksheet(request, worksheet_id):
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="simple_table_grid.pdf"'

    #doc = SimpleDocTemplate(response, pagesize=letter)

    #    elements = []
    styles = getSampleStyleSheet()

    #Two Columns

    #    frame_title = Frame(doc.leftMargin, doc.height + 50, doc.width, 25, id='title', showBoundary=0)
    #    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height - 30, id='col1', showBoundary=0)
    #    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height - 30, id='col2', showBoundary=0)

    worksheet = Worksheet.objects.get(pk=worksheet_id)
    worksheet_name = worksheet.get_worksheet_name()
    worksheetInstance = globals()[worksheet_name]()
    worksheetInstance.number_of_exercises = worksheet.number_of_exercises
    worksheetInstance.level = worksheet.level

    #ptext = '<font size=10 color=#F00>%s - Level %s</font>' % (worksheet_name, worksheet.level.level_name)
    #elements.append(Paragraph(ptext, styles["Normal"]))

    #h1 = ParagraphStyle(name='test', fontSize=10, leading=16, alignment=2, rightIndent=20, fixedWidth=100)

    termsList = worksheetInstance.getTerms()


    #for t in termsList:

    #     data = []
    #     data.append([t.term1, t.operator, t.term2, '='])
    #     tbl = Table(data)
    #     tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1), 15),
    #                            ('BOTTOMPADDING',(0,0),(-1,-1), 10),
    #                             ('TEXTCOLOR',(0,0),(-1,-1),colors.black)]))
    #     elements.append(tbl)

    # for t in termsList:
    #     data = []
    #     data.append(['', t.term1])
    #     data.append([t.operator, t.term2])
    #
    #     tbl = Table(data)
    #     tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1), 15),
    #                             ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    #                              ('TEXTCOLOR',(0,0),(-1,-1),colors.black)]))
    #     elements.append(tbl)
    #     line = MCLine(50)
    #     elements.append(line)
    #     elements.append(Spacer(100, 23, isGlue=True))

    #    doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame_title, frame1,frame2]), ])

    #elements = getFormattedElements(termsList, 'MULTIPLE_LINES')
    #doc = getDocTemplate(response, 'FOUR_COLUMNS')

    elements = getFormattedElements(termsList, worksheetInstance.getElementsTemplate())
    doc = getDocTemplate(response, worksheetInstance.getDocTemplate())

    nc = NumberedCanvas
    nc.worksheet_name = '%s - Level %s' % (worksheet_name, worksheet.level.level_name)
    doc.build(elements, canvasmaker=nc)

    return response


def contact(request):
    if request.method == 'POST':

        form = ContactForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass

            #send_mail(form.cleaned_data["subject"], form.cleaned_data["message"], form.cleaned_data["sender"], ['admin@mathimize.com'], fail_silently=False)
            sg = sendgrid.SendGridClient('app23000735@heroku.com', '5wqtuwsb')

            message = sendgrid.Mail()
            message.add_to('Mathimize <admin@mathimize.com>')
            message.set_subject(form.cleaned_data["subject"])
            message.set_html(form.cleaned_data["message"])
            message.set_text(form.cleaned_data["message"])
            message.set_from(form.cleaned_data["sender"])
            status, msg = sg.send(message)

            return HttpResponseRedirect('/thankyou/')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, })


class MCLine(Flowable):
    #Line flowable --- draws a line in a flowable
    #http://two.pairlist.net/pipermail/reportlab-users/2005-February/003695.html
    #----------------------------------------------------------------------
    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    #----------------------------------------------------------------------
    def __repr__(self):
        return "Line(w=%s)" % self.width

    #----------------------------------------------------------------------
    def draw(self):
        x = (self._frame.width - self.width) / 2
        self.canv.line(x, self.height, x + self.width, self.height)


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
            term1 = self.getDifferentRandomTerm(previousTerm, 1, 9)
            previousTerm = term1
            t = Terms(term1, term1, "+")
            termsList.append(t)

        return termsList

    def getDocTemplate(self):
        return 'TWO_COLUMNS'

    def getElementsTemplate(self):
        return 'SINGLE_LINE'


class Subtraction(Worksheet):
    def getTerms(self):
        termsList = []
        for i in range(self.number_of_exercises):
            if self.level.level_name == 'I':
                maxInt = 9
                minInt = 1
            if self.level.level_name == 'II':
                maxInt = 99
                minInt = 10

            if self.level.level_name == 'III':
                maxInt = 999
                minInt = 100

            term1 = random.randint(minInt, maxInt)
            term2 = self.getDifferentRandomTerm(term1, minInt, maxInt)
            if (term1 < term2):
                temp = term2
                term2 = term1
                term1 = temp

            t = Terms(term1, term2, "-")
            termsList.append(t)

        return termsList

    def getDocTemplate(self):
        if self.level.level_name == 'II':
            return 'FOUR_COLUMNS'
        return 'TWO_COLUMNS'

    def getElementsTemplate(self):
        if self.level.level_name == 'II':
            return 'MULTIPLE_LINES'
        return 'SINGLE_LINE'


class Addition(Worksheet):
    def getTerms(self):
        termsList = []
        for i in range(self.number_of_exercises):
            if self.level.level_name == 'I':
                maxInt1 = 9
                minInt1 = 1
                maxInt2 = 9
                minInt2 = 1

            elif self.level.level_name == 'II':
                maxInt1 = 19
                minInt1 = 11
                maxInt2 = 9
                minInt2 = 1

            elif self.level.level_name == 'III':
                maxInt1 = 99
                minInt2 = 11
                maxInt2 = 9
                minInt2 = 1
            elif self.level.level_name == 'IV':
                maxInt1 = 99
                minInt1 = 11
                maxInt2 = 99
                minInt2 = 11


            term1 = random.randint(minInt1, maxInt1)
            term2 = self.getDifferentRandomTerm(term1, minInt2, maxInt2)
            t = Terms(term1, term2, "+")
            termsList.append(t)
        return termsList

    def getDocTemplate(self):
        if self.level.level_name == 'III':
            return 'FOUR_COLUMNS'
        return 'TWO_COLUMNS'

    def getElementsTemplate(self):
        if self.level.level_name == 'III':
            return 'MULTIPLE_LINES'
        return 'SINGLE_LINE'


