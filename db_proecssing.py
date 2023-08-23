#def display_table(cur_obj,table_name,column=None):
#def show_tables(cur_obj):
from datetime import datetime

# def insert_purchase(cur,conn,p_id,t_s,id,qty,cp,amount):
    
#     conn.commit();



def show_time():
    now = datetime.now()
    time_date =str(now.day) +'/'+str(now.month)+'/'+str(now.year)+'-'+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
    return time_date;

def generate_id(cur,table_name):
    temp = cur.execute("select * from {}".format(table_name))
    ls = temp.fetchall();
    if(ls == []):
        return table_name+'_id_'+str(1);
    else:
        return table_name+'_id_'+str(int(ls[-1][0].replace("{}_id_".format(table_name),""))+1)

def show_tables(cur_obj):
    cur_obj.execute("select name from sqlite_master where type = 'table'")
    temp = [i[0] for i in cur_obj.fetchall()]; #when fetching [('company',), ('Item',), ('purchase',), ('sales',)]
    return (temp);

def display_table(cur_obj,table_name,column=None):
    if(column == None):
        query = ("select * from {}".format(table_name))
    else:
        query = "select ";
        for i in range(len(column)):
            if(i == len(column)-1):
                query+=column[i];
            else:
                query+=(column[i]+",")
        query += " from {}".format(table_name);
    cur_obj.execute(query);
    ls = cur_obj.fetchall();
    heading = [i[0] for i in cur_obj.description]
    # print(cur_obj.description); (('Time_stamp', None, None, None, None, None, None), ('Item_ID', None, None, None, None, None, None), ('Item_Name', None, None, None, None, None, None), ('Quantity', None, None, None, None, None, None), ('Rate', None, None, None, None, None, None), ('Amount', None, None, None, None, None, None))
    # print(ls) #[('item_id_1', 'Pen'), ('item_id_2', 'Pencil'), ('item_id_3', 'Eraser'), ('item_id_4', 'Sharpener'), ('item_id_5', 'Geometry box')]
    return heading,ls;



def show_money(cur,id):
    cur.execute("select rate from purchase where item_id = '{}'".format(id))
    ls = cur.fetchall()
    if(len(ls) == 0):
        return 0;
    else:
        return ls[-1][0];


def isemptytable(cur,table_name):
    cur.execute("select * from {}".format(table_name))
    if(cur.fetchall() == []):
        return True;
    else:
        return False;

def countrowintable(cur,table_name):
    cur.execute("select * from {}".format(table_name));
    return (len(cur.fetchall()));

def product_details(cur,item_id):
    cur.execute("select item_name,Quantity from item where item_id = '{}'".format(item_id))
    temp = cur.fetchall()
    return temp[0][0],temp[0][1];

def available_balance(cur,c_name):
    print("Cname",c_name)
    cur.execute("select cash_balance from company where company_name = '{}'".format(c_name))
    ans = cur.fetchall()[0][0]
    return ans;
