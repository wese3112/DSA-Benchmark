# -*- coding: utf-8 -*-

from __future__ import division
from scipy.stats import randint
import matplotlib.pyplot as plt
import numpy as np
from xml.dom import minidom
import os
import dsa_htmlreport as dsahtml

class Character:
    def __init__(self, charactername):
        try:
            #charXML = minidom.parse(xmlfile)
            charXML = minidom.parse('characters/dsachar_'+charactername+'/DSA_char_'+charactername+'.xml')
            charData = charXML.getElementsByTagName('charakter')[0]

            self.name = str(charData.attributes['name'].value)

            self.properties = dict()
            for prop in charData.getElementsByTagName('eigenschaft'):
                self.properties[str(prop.attributes['name'].value)] = int(prop.firstChild.data)

            charTalents = charData.getElementsByTagName('talente')
            self.talents = dict()
            for talentNode in charTalents:
                talent = talentNode.getElementsByTagName('talent')[0]
                talentValue = talentNode.getElementsByTagName('talentwert')[0]
                test = talentNode.getElementsByTagName('probe')[0]
                self.talents[str(talent.firstChild.data)] = (int(talentValue.firstChild.data),
                                                             str(test.firstChild.data))
        except BaseException as e:
            print 'Error', e

    def modify(self, talent, modrange=7):
        orig_taw = self.talents[talent][0]
        winchances = []
        barcolors = []
        for mod in range(-modrange,modrange):
            self.talents[talent] = (orig_taw+mod, self.talents[talent][1])
            results = self.__benchmarkfun(talent, benchmarksize=10000)
            wins, fails = self.__chance(results)
            winchances.append(wins/100)
            if mod == 0:
                barcolors.append('red')
            else:
                barcolors.append('blue')
        self.talents[talent] = (orig_taw, self.talents[talent][1])
        plt.bar(range(orig_taw-modrange,orig_taw+modrange), winchances, align='center', color=barcolors, alpha=0.6)
        plt.grid()
        plt.xticks(np.arange(orig_taw-modrange, orig_taw+modrange+1, 1.0))
        plt.xlabel('TaW Modifikation')
        plt.ylabel('Gewinnchance [%]')
        plt.title('Auswirkung von TaW-Modifikationen, Talent: '+talent)
        plt.yticks(np.arange(0, 100, 10))
        plt.savefig('characters/dsachar_'+self.name+'/histograms/'+ talent + '_modified.png')
        plt.close()

    def test(self, talent, *throws):
        tests = self.talents[talent][1].split(',')
        testvalues = [self.properties[test] for test in tests]
        talentvalue = self.talents[talent][0]
        throwcnt = 0

        print '###################################################'
        print 'Test auf          ', talent, 'beginnt'
        print 'Tests:            ', tests
        print 'TaW:              ', talentvalue
        print 'Eigenschaftswerte:', testvalues

        if talentvalue < 0: # subtract from all testvalues
            testvalues = [testvalue + talentvalue for testvalue in testvalues]
            talentvalue = 0 # DEBUG
            print 'Testwerte        :', testvalues, '(wg. negativem TaW)'

        for throw in throws:
            print 'Wurf:', throw,
            if throw > testvalues[throwcnt]:
                talentvalue = talentvalue - (throw - testvalues[throwcnt])
                print 'Nicht geschafft, TaW -', (throw-testvalues[throwcnt])
            else: # win
                print 'Geschafft!'
            throwcnt = throwcnt+1

        if talentvalue >= 0:
            print 'Erfolg!', talentvalue, 'TaW-Punkte übrig'
        else:
            print 'Fehlschlag mit', talentvalue, 'TaW-Punkten'

        return talentvalue

    def test_silent(self, talent, *throws):
        tests = self.talents[talent][1].split(',')
        testvalues = [self.properties[test] for test in tests]
        talentvalue = self.talents[talent][0]
        throwcnt = 0

        if talentvalue < 0: # subtract from all testvalues
            testvalues = [testvalue + talentvalue for testvalue in testvalues]
            talentvalue = 0 # DEBUG

        for throw in throws:
            if throw > testvalues[throwcnt]:
                talentvalue = talentvalue - (throw - testvalues[throwcnt])
            throwcnt = throwcnt+1
        return talentvalue

    def __chance(self, results):
        wins = 0
        fails = 0
        for result in results:
            if result >= 0:
                wins = wins + 1
            else:
                fails = fails + 1
        return (wins, fails)

    def __benchmarkfun(self, talent, benchmarksize):
        R1 = randint.rvs(1, 20, size=benchmarksize)
        R2 = randint.rvs(1, 20, size=benchmarksize)
        R3 = randint.rvs(1, 20, size=benchmarksize)
        R = zip(R1, R2, R3)
        testcount = 1
        testresults = []
        for throw in R:
            testcount += 1
            testresults.append(self.test_silent(talent, throw[0], throw[1], throw[2]))
        return testresults

    def benchmark(self, benchmarksize=50000, debug=False):
        benchmark = dict()
        chances = dict()

        if debug: benchmarksize=1000

        # HTML Report generation
        html = ''
        html += dsahtml.header(self.name)
        html += dsahtml.benchmarkheader(self.name, benchmarksize)
        html += dsahtml.propertiestable(self.properties)
        if debug:
            talents = ['klettern', 'sinnesschaerfe', 'athletik']
        else:
            talents = self.talents.keys()

        for talent in talents:
            print 'Test auf %20s ->' % (talent),
            benchmark[talent] = self.__benchmarkfun(talent, benchmarksize)
            chances[talent] = self.__chance(benchmark[talent])
            print 'wins: %6d, fails: %6d' % (chances[talent][0], chances[talent][1]),
            print 'win-chance:', (chances[talent][0]/benchmarksize)*100, '%'
            bins = max(benchmark[talent])-min(benchmark[talent])+1
            histogram_range = (min(benchmark[talent])-0.5, max(benchmark[talent])+0.5)
            plt.hist(benchmark[talent], bins, histtype='step', range=histogram_range, rwidth=0.3, cumulative=-1, normed=True, align='mid', color='blue')
            plt.hist(benchmark[talent], bins, range=histogram_range, rwidth=0.3, normed=True, align='mid', color='red')
            plt.legend(('kumulativ', 'normal'), loc=3)
            plt.grid()
            plt.yticks(np.arange(0, 1.0, 0.1))
            plt.xlabel('Verbliebene Talentwerte')
            plt.ylabel('Probenanzahl')
            plt.title(self.name+' Talent-Benchmark: '+talent)
            plt.savefig('characters/dsachar_'+self.name+'/histograms/'+ talent + '_histogram.png')
            plt.close()
            self.modify(talent)

        # create a sorted list from dict
        # sorted by win-chance
        chances_sorted_winchance = sorted(chances, key=chances.get)
        chances_sorted_winchance.reverse()
        chances_sorted_alphabet = sorted(chances.keys())
        html += dsahtml.overview(zip(chances_sorted_winchance, chances_sorted_alphabet), chances)

        for talent in chances_sorted_alphabet:
            taw = self.talents[talent][0]
            tests = self.talents[talent][1]
            props = tests.split(',')
            p1 = self.properties[props[0]]
            p2 = self.properties[props[1]]
            p3 = self.properties[props[2]]
            if taw < 0:
                props = (p1+taw, p2+taw, p3+taw)
            else:
                props = (p1, p2, p3)
            wins = chances[talent][0]
            fails = chances[talent][1]
            winchance= wins/(wins+fails)*100
            html += dsahtml.talenttable(talent, taw, tests, props, wins, fails, winchance)

        html += dsahtml.footer()
        fname = 'characters/dsachar_'+self.name+'/benchmark_'+self.name+'.html'
        f = open(fname, 'w')
        f.write(html)
        f.close()
        print 'DATEI GESCHRIEBEN:', fname
        return 1

def __userInput(talentart, talenttyp, newCharXML, charBase, talentDatabase):
    for talent in talentDatabase:
        tname = talent.getElementsByTagName('talent')[0].firstChild.data
        tart = talent.getElementsByTagName('talent')[0].attributes['art'].value
        ttyp = talent.getElementsByTagName('talent')[0].attributes['typ'].value
        tprobe = talent.getElementsByTagName('probe')[0].firstChild.data
        if talentart == str(tart) and talenttyp == str(ttyp):
            print 'Talentwert für', tname,
            userTalentValue = raw_input(': ')
            if userTalentValue == 'x':
                continue
            __addTalent(tart, ttyp, tname, tprobe, userTalentValue, newCharXML, charBase)

def __addTalent(talentart, talenttyp, tname, tprobe, userTalentValue, newCharXML, charBase):
    charTalents = newCharXML.createElement('talente')
    # add talent
    newTalent = newCharXML.createElement('talent')
    newTalent.setAttribute('art', talentart)
    newTalent.setAttribute('typ', talenttyp)
    newTalent.appendChild(newCharXML.createTextNode(tname))
    charTalents.appendChild(newTalent)
    # add talent value
    talentvalue = newCharXML.createElement('talentwert')
    talentvaluetext = newCharXML.createTextNode(userTalentValue)
    talentvalue.appendChild(talentvaluetext)
    charTalents.appendChild(talentvalue)
    # add test values
    probe = newCharXML.createElement('probe')
    probevalue = newCharXML.createTextNode(str(tprobe))
    #probe.appendChild(newCharXML.createTextNode(str(tprobe)))
    probe.appendChild(probevalue)
    charTalents.appendChild(probe)
    # append to character
    charBase.appendChild(charTalents)

def createNewChar():
    print '\n\nIm folgenden werden dir Fragen zur Erstellung deines Charakters gestellt'
    print '########################################################################\n'
    # create new xml file structure
    newCharXML = minidom.Document()
    charBase = newCharXML.createElement('charakter')

    charName = raw_input('Name des charakters: ')
    charBase.setAttribute('name', charName)

    # ask for character properties
    properties = ['mu', 'kl', 'in', 'ch', 'ff', 'ge', 'ko', 'kk']

    print '\n\nCharaktereigenschaften angeben:'
    print '###############################\n'
    for prop in properties:
        charProps = newCharXML.createElement('eigenschaft')
        charProps.setAttribute('name', prop)
        propvalue = newCharXML.createTextNode(raw_input(prop+': '))
        charProps.appendChild(propvalue)
        charBase.appendChild(charProps)

    # load talent database
    talentDatabaseXML = minidom.parse('characters/DSA_alle_talente.xml')
    talentDatabase = talentDatabaseXML.getElementsByTagName('talente')

    print '\n\nKörerliche Basistalente angeben:'
    print '####################################\n'
    __userInput('koerperlich', 'basis', newCharXML, charBase, talentDatabase)

    print '\nKörerliche Spezialtalente angeben:'
    print '\'x\' eingeben, wenn Talent nicht verfügbar'
    print '###########################################\n'
    __userInput('koerperlich', 'spezial', newCharXML, charBase, talentDatabase)

    print '\n\nGesellschaftliche Basistalente angeben:'
    print '###########################################\n'
    __userInput('gesellschaftlich', 'basis', newCharXML, charBase, talentDatabase)

    print '\nGesellschaftliche Spezialtalente angeben:'
    print '\'x\' eingeben, wenn Talent nicht verfügbar'
    print '###########################################\n'
    __userInput('gesellschaftlich', 'spezial', newCharXML, charBase, talentDatabase)

    print '\nGesellschaftliche Berufe angeben:'
    print '\'x\' eingeben, wenn Beruf nicht verfügbar'
    print '##########################################\n'
    __userInput('gesellschaftlich', 'beruf', newCharXML, charBase, talentDatabase)

    print '\n\nNatur Basistalente angeben:'
    print '###########################################\n'
    __userInput('natur', 'basis', newCharXML, charBase, talentDatabase)

    print '\nNatur Spezialtalente angeben:'
    print '\'x\' eingeben, wenn Talent nicht verfügbar'
    print '###########################################\n'
    __userInput('natur', 'spezial', newCharXML, charBase, talentDatabase)

    print '\nNatur Berufe angeben:'
    print '\'x\' eingeben, wenn Beruf nicht verfügbar'
    print '##########################################\n'
    __userInput('natur', 'beruf', newCharXML, charBase, talentDatabase)

    print '\n\nWissens-Basistalente angeben:'
    print '###########################################\n'
    __userInput('wissen', 'basis', newCharXML, charBase, talentDatabase)

    print '\nWissens-Spezialtalente angeben:'
    print '\'x\' eingeben, wenn Talent nicht verfügbar'
    print '###########################################\n'
    __userInput('wissen', 'spezial', newCharXML, charBase, talentDatabase)

    print '\nWissens-Berufe angeben:'
    print '\'x\' eingeben, wenn Beruf nicht verfügbar'
    print '##########################################\n'
    __userInput('wissen', 'beruf', newCharXML, charBase, talentDatabase)

    print '\n\nHandwerkliche Basistalente angeben:'
    print '###########################################\n'
    __userInput('handwerklich', 'basis', newCharXML, charBase, talentDatabase)

    print '\nHandwerkliche Spezialtalente angeben:'
    print '\'x\' eingeben, wenn Talent nicht verfügbar'
    print '###########################################\n'
    __userInput('handwerklich', 'spezial', newCharXML, charBase, talentDatabase)

    print '\nHandwerkliche Berufe angeben:'
    print '\'x\' eingeben, wenn Beruf nicht verfügbar'
    print '##########################################\n'
    __userInput('handwerklich', 'beruf', newCharXML, charBase, talentDatabase)

    # prepare XML
    newCharXML.appendChild(charBase)

    charNames = charName.split()
    filename = charNames.pop(0)
    for name in charNames:
        filename = filename+name

    os.mkdir('characters/dsachar_'+filename)
    os.mkdir('characters/dsachar_'+filename+'/histograms')
    f = open('characters/dsachar_'+filename+'/DSA_char_'+filename+'.xml', 'w')
    print 'Ordner characters/dsachar_%s erstellt'%filename
    print 'Ordner characters/dsachar_%s/histograms erstellt'%filename
    print 'Datei  characters/dsachar_%sDSA_char_ erstellt'%filename
    newCharXML.writexml(f)
    f.close()

if __name__ == '__main__':
	pass
