# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 14:06:59 2013

@author: sebastian
"""
from __future__ import division
import time

def header(name):
    htmlcode = """\n<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                <html>
                  <head>
                    <meta content="text/html; charset=utf-8" http-equiv="content-type">
                    <title>DSA Tool - Benchmark: %s</title>
                    <style type="text/css">
                      @import "../bmstyle.css"
                    </style>
                  </head>
                  <body>
                  """%str(name)
    return htmlcode
    
def talenttable(talent,taw,tests,testvalues,wins,fails,winchance):
    htmlcode = """<table border="1" width="100%%">
              <tbody>
                <tr>
                  <td class="talhead" colspan="4" rowspan="1"><a id="%s">%s</a></td>
                </tr>
                <tr>
                  <th colspan="2" rowspan="1">Histogramm </th>
                  <th colspan="2" rowspan="1">TaW-Modkfikation </th>
                </tr>
                <tr>
                  <td style="text-align: center;" colspan="2" rowspan="1"><img title="%s_histogramm"
                      src="histograms/%s_histogram.png" width="400"><br>
                  </td>
                  <td style="text-align: center;" colspan="2" rowspan="1"><img title="%s_modified"
                      src="histograms/%s_modified.png" width="400"><br>
                  </td>
                </tr>
                <tr>
                  <th colspan="4" rowspan="1">Übersicht </th>
                </tr>
                <tr>
                  <td class="descript">Talentwert</td>
                  <td class="values">%s</td>
                  <td style="width: 173.467px;" class="descript">Gewinnchance</td>
                  <td class="values" style="width: 345.75px;">%s</td>
                </tr>
                <tr>
                  <td style="width: 188.65px;" class="descript">Probe auf Talente</td>
                  <td class="values" style="width: 333.517px;">%s</td>
                  <td class="descript">Gewonnene Proben</td>
                  <td class="values">%s</td>
                </tr>
                <tr>
                  <td class="descript">Probe auf Werte</td>
                  <td class="values">%s</td>
                  <td class="descript">Verlorene Proben</td>
                  <td class="values">%s</td>
                </tr>
                <tr>
                    <td style="text-align: right;" colspan="4"><a class="values" href="#zusammenfassung">Zurück zur Zusammenfassung</a></td>
                </tr>
                  </tbody>
                </table><br><br>
                """%(talent,talent,talent,talent,talent,talent,
                     str(taw),str(winchance)+'%',tests,str(wins),str(testvalues),str(fails))
    return htmlcode

def benchmarkheader(name, benchmarksize):
    ltime = time.localtime()
    datum = str(ltime.tm_mday)+'.'+str(ltime.tm_mon)+'.'+str(ltime.tm_year)
    datum += ', '+str(ltime.tm_hour)+':'+str(ltime.tm_min)+'UHR'
    html = """<table style="width: 100%%;" border="1">
          <tbody>
            <tr>
              <td class="talhead" colspan="4" rowspan="1">DSA Tool - Benchmark<br>
                %s</td>
            </tr>
            <tr>
              <th>Datum</th>
              <td class="descript">%s</td>
              <th>Benchmarkumfang</th>
              <td class="descript">%d</td>
            </tr>
          </tbody>
        </table><br><br>"""%(name,datum,benchmarksize)
    return html
    
def propertiestable(props):
    html = """    <table border="1" width="100%%">
          <tbody>
            <tr>
              <td class="talhead" colspan="8" rowspan="1">Eigenschaften</td>
            </tr>
            <tr>
              <th>MU</th>
              <th>KL</th>
              <th>IN</th>
              <th>CH</th>
              <th>FF</th>
              <th>GE</th>
              <th>KO</th>
              <th>KK</th>
            </tr>
            <tr class="props">
              <td class="props">%d</td>
              <td class="props">%d</td>
              <td class="props">%d</td>
              <td class="props">%d</td>
              <td class="props">%d</td>
              <td class="props">%d</td>
              <td class="props">%d</td>
              <td class="props">%d</td>
            </tr>
          </tbody>
        </table><br><br>"""%(props['mu'],props['kl'],props['in'],props['ch'],props['ff'],
                     props['ge'],props['ko'],props['kk'])
    return html
        
def overview(talents,chances):
    html = """    <table border="1" width="100%%">
              <tbody>
                <tr>
                  <td class="talhead" colspan="4" rowspan="1" id="zusammenfassung">Zusammenfassung</td>
                </tr>
                <tr>
                  <th colspan="2" rowspan="1">Sortiert nach Gewinnchance </th>
                  <th colspan="2" rowspan="1">Alphabetisch Sortiert</th>
                </tr>
                <tr>
                  <td style="width: 200px;" class="descript">Talent</td>
                  <td class="descript">Gewinnchance</td>
                  <td style="width: 200px;" class="descript">Talent</td>
                  <td class="descript">Gewinnchance</td>
                </tr>
            """
            
    for talent in talents:
        tmpchan0 = (chances[talent[0]][0]/(chances[talent[0]][0]+chances[talent[0]][1]))*100
        tmpchan1 = (chances[talent[1]][0]/(chances[talent[1]][0]+chances[talent[1]][1]))*100
        html += """<tr>
                    <td class="values">%s</td>
                      <td>
                        <div class="progbar" style="width:%d%%">%d%%</div>
                      </td>
                      <td class="values"><a href="#%s">%s</a></td>
                      <td>
                        <div class="progbar" style="width:%d%%">%d%%</div>
                      </td>
                    </tr>
                """%(talent[0],tmpchan0,tmpchan0,talent[1],talent[1],tmpchan1,tmpchan1)
    html +="""
              </tbody>
            </table><br><br><br>
            """
    return html

def footer():
    htmlcode = """</body>
                </html>"""
    return htmlcode
    
if __name__=='__main__':
    talent = 'sinnesschaerfe'
    taw = 7
    tests = 'ge,kk,ko'
    winchance = 87
    testvalues = (12,13,12)
    wins = 235
    fails = 632
    html = ''
#    html += header('Vracass')
#    html += talenttable(talent,taw,tests,testvalues,wins,fails,winchance)
#    html += footer()
    html += benchmarkheader('Vracass', 100)
    print html
    f = open('characters/dsachar_Vracass/myhtml.html', 'w')
    f.write(html)
    f.close()