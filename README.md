# PDFGenerator-API

This api will generate a sample pdf consisting of 2 Tables and will send it in a response to client.
(Cross-Domain/Site Enabled)

#### main route:

`/generate`:  
This route will generate a pdf containing 2 tables with pre-defined hard coded data.

This route can either be accessed with 'GET' or 'POST' request.  
#### 1] 'GET' :  
Accessing with this request will generate pdf with predefined data.  
#### 2] 'POST' :  
Accessing with this request will generate pdf with given data.  
The Provided data will be used to create one row in second Table in the pdf.  
(PS: The first pdf will remain unchanged)  
Request Data can be a `FormData` or `Json`  
+ accepted paramters:  
  - `color` -- This is a string value (e.g.'Red')
  - `amount` -- This is a integer value (e.g. 67)
  - `price` --  This can be either a integer or string value (e.g. 399 or 'Rs.399')
