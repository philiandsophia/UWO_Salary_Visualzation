# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 16:55:11 2017

@author: choip
"""

import PyPDF2
import string
import heapq
import statistics
import matplotlib.pyplot as plt
import numpy as np
import pylab


def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def in_list(the_list, astring):
    a = 0 
    for e in astring:
        if e in the_list:
            a += 1 
    if a > 0:
        return True
    else:
        return False
    


def remove_after(the_list,pos,val):
    new_list = the_list[pos:]
    new_list.remove(val)
    the_list = the_list[:pos] + new_list
    return the_list


       
def consecutive_string(the_list):
    counter = 0
    where = 0
    d = list(string.ascii_uppercase)
    for e in the_list:
        if in_list(d,e):
            counter+=1
            where +=1
        if counter == 3:
            where = where - 1
            the_list = remove_after(the_list,where-1,e)
            counter = 0
        if '$' in e:
            counter = 0
            where += 1
    return the_list



dic = {}
a = [1,2,3,4,5,6]
b = ['a','b','v','d','f','e']


f = ['A','V','C','$12','$14','A','V','$13','$23','F','G','$34','$36','F','F','F','$23','$12','F','F','F']
#print (consecutive_string(f))

pdfFile = open('uwo_salaries.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(pdfFile)

pageObj = pdfReader.getPage(0)

text = pageObj.extractText().split()


remove_list = ['Cal', 'Year', 'Année', 'civile', 'Sector', 'Secteur', 'Employer', 'Employeur', 'Surname', 'Nom', 'de', 'famille', 'Given', 'Name', 'Prénom', 'Position', 'Title', 'Poste', 'Salary', 'Paid', 'Traitement', 'versé', 'Taxable', 'Benefits', 'Avantages', 'imposables', '2016', 'Universities', 'Universités', 'UNIVERSITY']
remove_list2 = ['RECORD', "EMPLOYEES'", 'SALARIES', 'AND', 'BENEFITS', 'REGISTRE', 'DES', 'TRAITEMENTS', 'ET', 'AVANTAGES', 'VERSÉS', 'AUX', 'EMPLOYÉS', 'EN', 'Please', 'refer', 'to', 'guide', 'Preparing', 'Your', 'Report', 'for', ',', 'Disclosure', 'Act', 'before', 'filling', 'out', 'this', 'form.', 'Se', 'reporter', 'au', 'guide', 'Préparation', 'du', 'rapport', 'aux', 'fins', 'la', 'Loi', '1996', 'sur', 'la', 'divulgation', 'des', 'traitements', 'dans', 'le', 'secteur', 'public', 'pour', 'remplir', 'la', 'présente', 'formule.', 'Insert', 'additional', 'rows', 'at', 'end', 'as', 'needed', 'Insérer', "d'autres", 'rangées', 'au', 'besoin']


a = remove_values_from_list(text,'Public')
a = remove_values_from_list(a,'Universités\nUNIVERSITY')
a = remove_values_from_list(a,'WESTERN')
a = remove_values_from_list(a,'OF')
a = remove_values_from_list(a,'/')
a = remove_values_from_list(a,'')
a = remove_values_from_list(a,'ONTARIO')
a = remove_values_from_list(a,'the')

for e in remove_list:
    a = remove_values_from_list(a,e)

for e in remove_list2:
    a = remove_values_from_list(a,e)

pageObj = pdfReader.getPage(1)

text= pageObj.extractText().split()

for e in text:
    e = e.strip()

b = remove_values_from_list(text,'Public')
b = remove_values_from_list(b,'Universités\nUNIVERSITY')
b = remove_values_from_list(b,'WESTERN')
b = remove_values_from_list(b,'OF')
b = remove_values_from_list(b,'/')
b = remove_values_from_list(b,'')
b = remove_values_from_list(b,'ONTARIO')
b = remove_values_from_list(b,'the')
b = remove_values_from_list(b,'UNIVERSITY')
b = remove_values_from_list(b,'Universities')
b = remove_values_from_list(b,'Universités')
b = remove_values_from_list(b,'2016')

c = []
d = []

for i in range(2,26):
    pageObj = pdfReader.getPage(i)
    text = pageObj.extractText().split()
    for e in text:
        e = e.strip()
        d = remove_values_from_list(text,'Public')
        d = remove_values_from_list(d,'Universités\nUNIVERSITY')
        d = remove_values_from_list(d,'WESTERN')
        d = remove_values_from_list(d,'OF')
        d = remove_values_from_list(d,'/')
        d = remove_values_from_list(d,'')
        d = remove_values_from_list(d,'ONTARIO')
        d = remove_values_from_list(d,'the')
        d = remove_values_from_list(d,'UNIVERSITY')
        d = remove_values_from_list(d,'Universities')
        d = remove_values_from_list(d,'Universités')
        d = remove_values_from_list(d,'2016')
    c = c+d
    d = []
 
c = c+b+a
number = ['1','2','3','4','5','6','7','8','9','0']
c = [e for e in c if e.isupper() or in_list(number,e)]
c = [e for e in c if not e.endswith('.')]
c = remove_values_from_list(c,'TA')
c = remove_values_from_list(c,'DE')
c = consecutive_string(c)

good_list = []
for i in range(len(c)):
    if i % 2 == 0:
        good_list.append(c[i])

money_list = [e.replace(',','') for e in good_list if '$' in e]
money_list = [e.replace('$','') for e in money_list]
money_list = [float(e) for e in money_list]
person_list = [e for e in good_list if '$' not in e]

good_dict = dict(zip(money_list,person_list))


top_10 = heapq.nlargest(10,money_list)
top_10_person = []

for e in top_10:
    top_10_person.append(good_dict[e])

sum_of_salary = 0 
for keys in good_dict:
    sum_of_salary += keys 

average_salary = sum_of_salary / len(good_dict)

std_deviation = statistics.pstdev(money_list)

a = top_10 + [147950.01]
b = top_10_person + ['Average']

print (list(zip(a,b)))


plt.hist(money_list, bins = 75)
plt.ylabel('Number of occurence')
plt.xlabel('Salary, $')
plt.title('Distribution of salary, 75 bins')

pylab.savefig('Salary_distribution.png')


