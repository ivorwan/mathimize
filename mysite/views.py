from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
#from polls.models import Choice, Poll
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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

# def some_view(request):
#     # response = HttpResponse(content_type='application/pdf')
#     # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#     # p = canvas.Canvas(response)
#     # p.drawString(100, 100, "Hello World.")
#     # p.showPage()
#     # p.save()
#     # return response
#     return


def generatePDFWorksheet(request, level):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="simple_table_grid.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))




    #termsList = locals().get("Level1")
    levelInstance = globals()[level]()

    #termsList = Level1().getTerms()
    termsList = levelInstance.getTerms()
    ptext = ""
    for t in termsList:
        ptext = '<font size=12>%s %s %s = <br/></font>' % (t.term1, t.operator, t.term2)
        elements.append(Paragraph(ptext, styles["Normal"]))
        elements.append(Spacer(1, 12))

    # write the document to disk
    doc.build(elements)
    return response


def generatePDF(request, rows, cols):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="simple_table_grid.pdf"'

    # doc = SimpleDocTemplate("simple_table_grid.pdf", pagesize=letter)
    doc = SimpleDocTemplate(response, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []

    data= [['00', '01', '02', '03', '04'],
       ['10', '11', '12', '13', '14'],
       ['20', '21', '22', '23', '24'],
       ['30', '31', '32', '33', '34']]

    t=Table(data)
    t.setStyle(TableStyle([('BACKGROUND',(1,1),(3,2),colors.green),
                           ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))

    elements.append(t)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))


    ptext = '<font size=12>ROWS: %s. <br/> COLS: %s</font>' % (rows, cols)


    elements.append(Paragraph(ptext, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # write the document to disk
    doc.build(elements)
    return response






class Level1:
    def getTerms(self):
        termsList = []
        t = Terms(2, 3, "+")

        termsList.append(t)

        t = Terms(5, 2, "+")
        termsList.append(t)

        t = Terms(1, 6, "+")
        termsList.append(t)

        t = Terms(2, 4, "+")
        termsList.append(t)

        t = Terms(8, 5, "+")
        termsList.append(t)

        return termsList


