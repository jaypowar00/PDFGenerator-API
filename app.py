from flask import Flask, send_file, redirect, url_for, request
from flask_cors import CORS
from fpdf import FPDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
CORS(app,expose_headers=['Access-Control-Allow-Origin'])

def styleWholeTable(table=Table,n=int):
    """
    #### usage: styleWholeTable(table=Table(),n=int)

    This styles the table.

    sets Borders,alignments, color, background color,font size and style

    accepts a Table variable created with Table()
    """
    #styling table
    style = TableStyle([
        ('BACKGROUND',(0,0),(-1,0),"#d3a15f"),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,0),14),
        ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige)
    ])
    table.setStyle(style)

    #aletrnate colors in rows
    rowNum = n
    for i in range(1, rowNum):
        if i%2==0:
            bc = colors.burlywood
        else:
            bc = colors.beige
        ts = TableStyle([('BACKGROUND',(0,i),(-1,i),bc)])
        table.setStyle(ts)
    
    #adding borders
    ts=TableStyle([
        # ('BOX',(0,0),(-1,-1),1,colors.black),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ])
    table.setStyle(ts)
    return table

def createStyledPdf(obj=[]):
    '''
    #### Usage: createpdf(list)

    This function creates a styled pdf with better look than the one created using fpdf library.
    
    This function also creates pdf containing 2 tables

    and 2nd table can have users values!

    list: list defines the contents to be included in 2nd table.  

    it contains color,number of boxes,Price(per box)

    `e.g. list = [['Red',30,'Rs.90'],['Black',46,'Rs.62'],...,[.,.,.]]`
    '''
    pdf = SimpleDocTemplate("pythonpdf.pdf",pagesize=letter)
    data = [
        ['First Name','Last Name','Age','Saraly'],
        ['Joe','Smith',24,'Rs.59400'],
        ['Klark','Kent',19,'Rs.89900']
    ]
    table = Table(data,spaceAfter=30)
    table = styleWholeTable(table,len(data))

    elems = []
    elems.append(table)
    #################
    # 2nd Table
    if obj:
        data = [['Color','Boxes','Prices\n(per 1 Box)']]
        for e in obj:
            if type(e)==list:
                data.append(e)
    else:
        data =  [
                ['Color','Boxes','Price\n(per 1 Box)'],
                ['Red',712,'Rs.30'],
                ['Blue',495,'Rs.45'],
                ['Black',398,'Rs.10']
                ]
    table = Table(data,spaceAfter=30)
    table = styleWholeTable(table,len(data))
    elems.append(table)

    pdf.build(elems)

def createpdf(obj=[]):
    '''
    #### Usage: createpdf(list)

    This function creates pdf containing 2 tables

    2nd table can have usrs values!

    list: list defines the contents to be included in 2nd table

    it contains color,number of boxes,Price(per box)

    `e.g. list = [['Red',30,'Rs.90'],['Black',46,'Rs.62'],...,[.,.,.]]`

    '''
    pdf=FPDF(format='letter', unit='in')
    pdf.add_page()
    pdf.set_font('Times','',10.0) 
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size

    data = [['First name','Last name','Age','City'],
    ['Jules','Smith',34,'San Juan'],
    ['Mary','Ramos',45,'Orlando'],[
    'Carlson','Banks',19,'Los Angeles']
    ]

    pdf.set_font('Times','B',14.0) 
    pdf.cell(epw, 0.0, 'Tables', align='C')
    pdf.ln(0.5)
    i=1
    for row in data:
        if i==1:
            pdf.set_font('Times','B',14.0)
            i=0
        else:
            pdf.set_font('Times','',12.0) 
        for datum in row:
            # Enter data in colums
            pdf.cell(col_width, 2*th, str(datum), border=1)
    
        pdf.ln(2*th)
    ##################################################################
    data = list()
    if obj:
        data = [['Color','Boxes','Prices\n(per 1 Box)']]
        for e in obj:
            if type(e)==list:
                data.append(e)
    else:
        data =  [
                ['Color','Boxes','Price\n(per 1 Box)'],
                ['Red',712,'Rs.30'],
                ['Blue',495,'Rs.45'],
                ['Black',398,'Rs.10']
                ]
    i=1
    pdf.ln(0.5)
    for row in data:
        if i==1:
            pdf.set_font('Times','B',14.0)
            i=0
        else:
            pdf.set_font('Times','',12.0) 
        for datum in row:
            # Enter data in colums
            pdf.cell(col_width, 2*th, str(datum), border=1)
    
        pdf.ln(2*th)

    pdf.output('pythonpdf.pdf')
    return True

@app.route('/')
def index():
    return "<h1>PDF from Api</h1><br><a href='/generate'>click here for pdf</a>"

@app.route('/generate',methods=['GET','POST'])
def create():
    if request.method=='POST':
        if request.form:
            form = request.form
            if 'color' in form and 'amount' in form and 'price' in form:
                color = form['color']
                amount = form['amount']
                price = form['price'] if type(form['price'])==str and 'Rs' in form['price'] else 'Rs.'+str(form['price']) if type(form['price'])==int or type(form['price'])==float or type(form['price'])==str else 'Rs.007'
                print(form['price'])
                print(type(form['price']))
        elif request.json:
            jsn = request.get_json()
            if 'color' in jsn and 'amount' in jsn and 'price' in jsn:
                color = jsn['color']
                amount = jsn['amount']
                price = jsn['price'] if type(jsn['price'])==str and 'Rs'in jsn['price'] else 'Rs.'+jsn['price'] if type(jsn['price'])==int or type(jsn['price'])==float else 'Rs.007'
        if form or jsn:
            row=[[color,amount,price]]
            # createpdf(row)
            createStyledPdf(row)
        else:
            # createpdf()
            createStyledPdf()
    else:
        # createpdf()
        createStyledPdf()
    try:
        return send_file('pythonpdf.pdf')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run()