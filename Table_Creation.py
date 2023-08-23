import sqlite3;
import db_proecssing as dp;
import os

# print(os.getcwd())
conn = sqlite3.connect("DataBase.db")
cur = conn.cursor()
def create():
    create_company_table = """create table company
    (
        Company_Name varchar,
        Cash_Balance Integer,
        Password varchar
    );
    """
    create_item_table = """create table Item
    (
        Item_ID varchar Primary Key,
        Item_Name varchar,
        Quantity integer
    )
    """
    create_purchase_table ="""create table purchase
    (
        Purchase_ID varchar Primary Key,
        Time_stamp varchar,
        Item_ID varchar,
        Quantity Integer,
        Rate Integer,
        Amount Integer
    )
    """
    create_sales_table = """create table sales
    (
        Sales_ID varchar,
        Time_Stamp varchar,
        Item_ID varchar,
        Quantity Integer,
        Rate Integer,
        Amount Integer 
    )
    """

    items = [('item_id_1','Pen'),('item_id_2','Pencil'),('item_id_3','Eraser'),('item_id_4','Sharpener'),('item_id_5','Geometry box'),]
    insert_item = """insert into Item values ('{}','{}',0);"""

    cur.execute(create_company_table)
    cur.execute(create_item_table)
    cur.execute(create_purchase_table)
    cur.execute(create_sales_table)

    for i in items:
        cur.execute(insert_item.format(i[0],i[1]))
        conn.commit();
    
# create();

# dp.display_table(cur,'item')
# dp.show_tables(cur)

