from flask import Flask, request
from searchIt import search
import html


app = Flask(__name__)

styles = """
<style> 
.site{
    font-size: .8rem;
    color: green;
}

.snippet{
    font-size: .9rem;
    color: grey;
    margin-bottom:30px;
}
.inputButtn{
    width: 10%; 
    height: 33px; 
    background-color: white; 
    border: 1px solid; 
    cursor: pointer;
    transition: 0.3s;
}
.inputButtn:hover {
    background-color: rgb(215, 212, 212);
}

.maindiv{
    width: 100%;
    text-align: center; 
    justify-content: center;
}

.logo{
    width: 30%; 
    height: 50%; 
    padding-top: 40px;
}

.inputField{
    width: 40%; 
    height: 30px;
}

.inputButtnAfterSearch{
    width: 10%; 
    height: 22px; 
    background-color: white; 
    border: 1px solid; 
    cursor: pointer;
    transition: 0.3s;
}
.inputButtnAfterSearch:hover {
    background-color: rgb(215, 212, 212);
}

.maindivAfterSearch{
    width: 100%;
    display: flex;
    text-align: left;
    /* justify-content: space-between; */
}

.logoAfterSearch{
    width: 5%; 
    height: 5%; 
    margin-top: -15px;
}

.inputFieldAfterSearch{
    width: 40%; 
    height: 20px;
}

.formSearch{
    width:100%;
}


</style>
"""

search_template = styles +"""
   <div class="maindivAfterSearch">
        <div class="inputAfterSearch" ></div>
             <img  class="logoAfterSearch" src="/static/images/logo_transparent.png">
            <form class="formSearch" action="/" method="post">
                <input class="inputFieldAfterSearch" type="text" name="query">
                <input class="inputButtnAfterSearch" type="submit" value="Go">
            </form>
        </div>
    </div>
"""

original_search_template = styles + """
    <div class="maindiv">
        <img class="logo" src="/static/images/logo_transparent.png">
        <div class="input">
            <form  action="/" method="post"  >
                <input class="inputField" type="text" name="query">
                <input class="inputButtn" type="submit" value="Go">
            </form>
        </div>
    </div>
"""

result_template="""
<p class="site">{rank} : {link} </p>
<a href="{link}"> {title} </a>
<p class="snippet"> {snippet} </p>
"""


def show_search_form():
    return original_search_template

def run_search_form(query):
    results = search(query)
    rendered = search_template
    # results["snippet"] = results["snippet"].apply(lambda x: html.escape(x)) # Can be deleted, this makes the browser not turn HTML tags to its actual original forme
    for index,row in results.iterrows():
        rendered += result_template.format(**row) # in search we have the columns that are made of link title etc. This will juste take those values and replace them in the template
    return rendered

@app.route("/",methods=["GET","POST"])
def search_form():
    if request.method == "POST" :
        query = request.form["query"]
        return run_search_form(query)
    else :
        return show_search_form()


    
