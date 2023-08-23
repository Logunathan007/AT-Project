from flask import Flask,render_template,url_for,request,redirect,send_file;
import db_proecssing as dp;
import Table_Creation as tc;
import sqlite3
conn = sqlite3.connect("DataBase.db",check_same_thread=False);
cur = conn.cursor();

app = Flask(__name__,template_folder="templates");

@app.route('/register',methods=["GET","POST"])
def register_page():
    if(request.method == 'POST'):
        name = request.form.get('name')
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')
        if(pass1 != pass2):
            return render_template("register.html",error = True,msg = "Password Didn't match")
        else:
            cur.execute("insert into company values ('{}',1000,'{}')".format(name,pass1))
            conn.commit();
            return render_template("login.html");
    return render_template("register.html");

@app.route('/',methods = ["GET","POST"])
def login_page():
    if(request.method == "POST"):
        name = request.form.get('name');
        pass1 = request.form.get('pass1');
        print("name is ",name,"pass ",pass1);
        temp = cur.execute("select * from company where (company_name = '{}' and password = '{}')".format(name,pass1))
        ls = temp.fetchall();
        if(ls == []):
            return render_template('login.html',error=True,msg="Wrong Credentials")
        else:
            login = True;
            Company_Name = name;
            return redirect('/home/'+name);

    return render_template('login.html');

@app.route('/home/<name>')
def home(name):
    amount = dp.available_balance(cur, name);
    heading,ls = dp.display_table(cur, "item")
    ls= [list(i) for i in ls];
    for i in ls:
        i.append(dp.show_money(cur,i[0]))

    return render_template("home.html",name = name,amount = amount,ls = ls);


@app.route('/add/<name>/')
def add(name):
    id = dp.generate_id(cur, 'item')
    cur.execute("insert into item values('{}','New',0)".format(id))
    conn.commit();
    return redirect("/home/"+name);

@app.route('/delete/<name>/<value>')
def delete(name,value):
    cur.execute("delete from item where item_id='{}'".format(value));
    conn.commit();
    return redirect("/home/"+name);

@app.route('/save/<value>/<name>')
def save(value,name):
    p_name = request.args.get("ch_name")
    print(name)
    cur.execute("update item set Item_Name='{}' where Item_Id='{}'".format(p_name,value))
    conn.commit();
    return redirect('/home/'+name)

@app.route('/purchase/<id>/<name>',methods=["POST","GET"])
def purchase(id,name):
    balance = dp.available_balance(cur,name);   #1000
    p_name,get_qty = dp.product_details(cur, id);   #logu #5
    if(request.method == "POST"):
        cp = int(request.form.get("cp"))  #5
        if(cp <= 0):
            return render_template("purchase.html",error=True,msg="Cost Price Must be greaten then zero",product_name=p_name,count=get_qty,balance=balance,id=id,name=name)
        qty = int(request.form.get("quantity"))  #10
        if(qty <= 0):
            return render_template("purchase.html",error=True,msg="Quantity Must be greater then zero ",product_name=p_name,count=get_qty,balance=balance,id=id,name=name)
        bal = balance-(cp*qty); 
        count = get_qty+qty   
        if(bal < 0):
            return render_template("purchase.html",error=True,msg="Insufficient Balance",product_name=p_name,count=get_qty,balance=balance,id=id,name=name)
        p_id = dp.generate_id(cur, "purchase")
        t_s = dp.show_time();
        amount = qty*cp;
        balance = bal;
        cur.execute("insert into purchase values('{}','{}','{}',{},{},{})".format(p_id,t_s,id,qty,cp,amount));
        cur.execute("update company set cash_balance={} where company_name='{}'".format(bal,name))
        cur.execute("update item set quantity={} where item_id='{}'".format(count,id));
        conn.commit();
    p_name,count = dp.product_details(cur, id);
    return render_template("purchase.html",product_name=p_name,count=count,balance=balance,id=id,name=name);

@app.route('/selling/<id>/<name>',methods=['GET',"POST"])
def selling(id,name):
    balance = dp.available_balance(cur,name);
    p_name,get_qty = dp.product_details(cur, id);
    cost_price = dp.show_money(cur, id)
    if(request.method == "POST"):
        if(get_qty <= 0):
            return render_template("selling.html",error=True,msg = "Insufficient Quantity",product_name=p_name,count=get_qty,balance=balance,id=id,name=name,cost_price=cost_price)
        sp = int(request.form.get("sp"))
        if(sp <= 0):
            return render_template("selling.html",error=True,msg = "Selling Price Must be Greater then or equal to one",product_name=p_name,count=get_qty,balance=balance,id=id,name=name,cost_price=cost_price)
        
        qty = int(request.form.get("quantity"))
        
        if(qty <= 0):
            return render_template("selling.html",error=True,msg = "Quantity Must be Greater then or equal to one",product_name=p_name,count=get_qty,balance=balance,id=id,name=name,cost_price=cost_price)
        ans = get_qty-qty
        if(ans < 0):
            return render_template("selling.html",error=True,msg = "Insufficient Quantity",product_name=p_name,count=get_qty,balance=balance,id=id,name=name,cost_price=cost_price)

        balance += (sp*qty)
        # print(get_qty,qty)
        
       
        s_id = dp.generate_id(cur, "sales")
        t_s = dp.show_time();
        amount = qty*sp;
        cur.execute("insert into sales values('{}','{}','{}',{},{},{})".format(s_id,t_s,id,ans,sp,amount));
        cur.execute("update company set cash_balance={} where company_name='{}'".format(balance,name))
        cur.execute("update item set quantity={} where item_id='{}'".format(ans,id));
        conn.commit();
    p_name,get_qty = dp.product_details(cur, id);
    return render_template("selling.html",product_name=p_name,count=get_qty,balance=balance,id=id,name=name,cost_price=cost_price);

@app.route("/purchase_history/<name>")
def purchase_history(name):
    heading,ls = dp.display_table(cur,"purchase as p left outer join item as i on(i.item_id=p.item_id)",column=['p.time_stamp','i.item_id','i.item_name','p.quantity','p.rate','p.amount'])
    s = []
    sub = ""
    for i in range(len(heading)):
        if(i == len(heading)-1):
            sub+=str(heading[i]);
        else:
            sub+=str(heading[i])+','
    s.append(sub);
    for j in ls[::-1]:
        sub = ""
        for i in range(len(j)):
            if(i == len(j)-1):
                sub+=str(j[i]);
            else:
                sub+=str(j[i])+','
        s.append(sub);
    f = open("Purchase.csv",'w')
    for i in s:
        f.write(i);
        f.write("\n")
    return render_template("history.html",table=ls[::-1],heading=heading,Title="Purchase",name=name);

@app.route("/selling_history/<name>")
def selling_history(name):
    heading,ls = dp.display_table(cur,"sales as s left outer join item as i on(i.item_id=s.item_id)",column=['s.time_stamp','i.item_id','i.item_name','s.quantity','s.rate','s.amount'])
    s = []
    sub = ""
    for i in range(len(heading)):
        if(i == len(heading)-1):
            sub+=str(heading[i]);
        else:
            sub+=str(heading[i])+','
    s.append(sub);
    for j in ls[::-1]:
        sub = ""
        for i in range(len(j)):
            if(i == len(j)-1):
                sub+=str(j[i]);
            else:
                sub+=str(j[i])+','
        s.append(sub);
    f = open("Selling.csv",'w')
    for i in s:
        f.write(i);
        f.write("\n")
    
    return render_template("history.html",table=ls[::-1],heading=heading,Title="Selling",name=name);

@app.route('/download/<f_name>')
def download(f_name):
    path = '{}.csv'.format(f_name)
    return send_file(path, as_attachment=True)

if(__name__ == "__main__"):
    if(dp.show_tables(cur) == []):
        tc.create();
    app.run(debug=True);
    

