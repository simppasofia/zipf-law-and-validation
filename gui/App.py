
from __future__ import division
import sys
from itertools import *
from pylab import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from scipy import stats
from scipy.stats import t, zipf
from scipy.optimize import curve_fit
from scipy.special import zetac

from nltk.corpus import reuters
from nltk.corpus import wordnet
import scipy.stats as ss
from scipy import special
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import tkinter as tk
from tkinter import ttk

import BL
from BL import zipf, linearRegression, general, histogram, fittingZipCurve, task7, task6, numberOfSenses



bookname1 = 'flatland.txt'
bookname2 = 'ulysses.txt'
bookname3 = 'panama.txt'
booklist = ["flatland.txt", "ulysses.txt", "panama.txt"]
catlist = ["flatlands_multi_category.txt", "ulysses_multi_category.txt", "panama_multi_category.txt"]



book1 = general.pick_book(bookname1)
book2 = general.pick_book(bookname2)
book3 = general.pick_book(bookname3)



tokens_with_count1 = general.tokenizer(book1)
tokens_with_count2 = general.tokenizer(book2)
tokens_with_count3 = general.tokenizer(book3)
ranks1, indices1, frequencies1 = general.token_counter(tokens_with_count1)
ranks2, indices2, frequencies2 = general.token_counter(tokens_with_count2)
ranks3, indices3, frequencies3 = general.token_counter(tokens_with_count3)
fitted_value1, lower_bound_fit1, upper_bound_fit1, upper_bound_pred1, lower_bound_pred1, r_squared1, new_r1, ci_level1 = linearRegression.linreg(ranks1, frequencies1, 0.975)
fitted_value2, lower_bound_fit2, upper_bound_fit2, upper_bound_pred2, lower_bound_pred2, r_squared2, new_r2, ci_level2 = linearRegression.linreg(ranks2, frequencies2, 0.975)
fitted_value3, lower_bound_fit3, upper_bound_fit3, upper_bound_pred3, lower_bound_pred3, r_squared3, new_r3, ci_level3 = linearRegression.linreg(ranks3, frequencies3, 0.975)

filtered_words1, ftokens_with_count1, topwords1, doclen1 = general.sw_filter(book1)
filtered_words2, ftokens_with_count2, topwords2, doclen2 = general.sw_filter(book2)
filtered_words3, ftokens_with_count3, topwords3, doclen3 = general.sw_filter(book3)
ranks1f, indices1f, frequencies1f = general.token_counter(ftokens_with_count1)
ranks2f, indices2f, frequencies2f = general.token_counter(ftokens_with_count2)
ranks3f, indices3f, frequencies3f = general.token_counter(ftokens_with_count3)
fitted_value1f, lower_bound_fit1f, upper_bound_fit1f, upper_bound_pred1f, lower_bound_pred1f, r_squared1f, new_r1f, ci_level1f = linearRegression.linreg(ranks1f, frequencies1f, 0.975)
fitted_value2f, lower_bound_fit2f, upper_bound_fit2f, upper_bound_pred2f, lower_bound_pred2f, r_squared2f, new_r2f, ci_level2f = linearRegression.linreg(ranks2f, frequencies2f, 0.975)
fitted_value3f, lower_bound_fit3f, upper_bound_fit3f, upper_bound_pred3f, lower_bound_pred3f, r_squared3f, new_r3f, ci_level3f = linearRegression.linreg(ranks3f, frequencies3f, 0.975)

LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x1000")
        selectedBook = StringVar()
        self.canvas = None
        label = tk.Label(self, text ="Zipf Law and validation 1", font = LARGEFONT)
        label.pack()
        def show(selection):
            global selectedBook
            selectedBook = clicked.get()
            myLabel.config(text=selectedBook)

        def callBack(t,y,u):
            global selectedBook
            selectedBook = clicked.get()
        def comboed(event):
            global selectedBook
            selectedBook = myCombo.get()

        def plotZip(selectedBook, useFilter):
            global canvas
            global fig

            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if(useFilter == 0):
                if selectedBook == "Flatland":
                    fig = zipf.zipf_plot(selectedBook, ranks1, frequencies1, fitted_value1,
                    upper_bound_fit1, lower_bound_fit1, upper_bound_pred1, lower_bound_pred1,0)
                elif selectedBook == "Ulysses":
                    fig = zipf.zipf_plot(selectedBook, ranks2, frequencies2, fitted_value2,
                    upper_bound_fit2, lower_bound_fit2, upper_bound_pred2, lower_bound_pred2,0)
                elif selectedBook == "Panama":
                    fig = zipf.zipf_plot(selectedBook, ranks3, frequencies3, fitted_value3,
                    upper_bound_fit3, lower_bound_fit3, upper_bound_pred3, lower_bound_pred3,0)
            else:
                if selectedBook == "Flatland":
                    fig = zipf.zipf_plot(selectedBook,ranks1f, frequencies1f, fitted_value1f,
                    upper_bound_fit1f, lower_bound_fit1f, upper_bound_pred1f, lower_bound_pred1f,1)
                elif selectedBook == "Ulysses":
                    fig = zipf.zipf_plot(selectedBook,ranks2f, frequencies2f, fitted_value2f,
                    upper_bound_fit2f, lower_bound_fit2f, upper_bound_pred2f, lower_bound_pred2f,1)
                elif selectedBook == "Panama":
                    fig = zipf.zipf_plot(selectedBook,ranks3f, frequencies3f, fitted_value3f,
                    upper_bound_fit3f, lower_bound_fit3f, upper_bound_pred3f, lower_bound_pred3f,1)


            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas.get_tk_widget().pack(pady=100)

        def plotHisto(selectedBook):
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            if selectedBook == "Flatland":
                fig = histogram.hist_plot(ftokens_with_count1,selectedBook)
            elif selectedBook == "Ulysses":
                fig = histogram.hist_plot(ftokens_with_count2,selectedBook)
            elif selectedBook == "Panama":
                fig = histogram.hist_plot(ftokens_with_count3,selectedBook)
            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas.get_tk_widget().pack(pady=100)

        def fitZipCurve(selectedBook):
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            if selectedBook == "Flatland":
                plt = fittingZipCurve.zipfcurve(selectedBook,ranks1, frequencies1, fitted_value1,
                upper_bound_fit1, lower_bound_fit1, upper_bound_pred1, lower_bound_pred1)
            elif selectedBook == "Ulysses":
                plt = fittingZipCurve.zipfcurve(selectedBook,ranks2, frequencies2, fitted_value2,
                upper_bound_fit2, lower_bound_fit2, upper_bound_pred2, lower_bound_pred2)
            elif selectedBook == "Panama":
                plt = fittingZipCurve.zipfcurve(selectedBook,ranks3, frequencies3, fitted_value3,
                upper_bound_fit3, lower_bound_fit3, upper_bound_pred3, lower_bound_pred3)
            self.canvas = FigureCanvasTkAgg(plt, master=self)
            self.canvas.get_tk_widget().pack(pady=100)

        def category(selectedBook):
           if self.canvas:
               self.canvas.get_tk_widget().destroy()
           if selectedBook == "Flatland":
               fig = task7.cat("flatland.txt", "flatlands_multi_category.txt")
           elif selectedBook == "Ulysses":
               fig = task7.cat("ulysses.txt", "ulysses_multi_category.txt")
           elif selectedBook == "Panama":
               fig = task7.cat("panama.txt", "panama_multi_category.txt")

           self.canvas = FigureCanvasTkAgg(fig, master=self)
           self.canvas.get_tk_widget().pack(pady=100)

        def expCutoff(selectedBook):
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if selectedBook == "Flatland":
                fig = task6.plot(ranks1f, frequencies1f, selectedBook)
            elif selectedBook == "Ulysses":
                fig = task6.plot(ranks2f, frequencies2f, selectedBook)
            elif selectedBook == "Panama":
                fig = task6.plot(ranks3f, frequencies3f, selectedBook)

            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas.get_tk_widget().pack(pady=100)
        def numberSenses(selectedBook):
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if selectedBook == "Flatland":
                fig = numberOfSenses.senses_plot(filtered_words1, frequencies1f, selectedBook)
            elif selectedBook == "Ulysses":
                fig = numberOfSenses.senses_plot(filtered_words2, frequencies2f, selectedBook)
            elif selectedBook == "Panama":
                fig = numberOfSenses.senses_plot(filtered_words3, frequencies3f, selectedBook)

            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas.get_tk_widget().pack(pady=100)

        options = [
        "Select Book","Flatland", "Ulysses", "Panama"
        ]
        myCombo = ttk.Combobox(self, value = options)
        myCombo.pack(pady=20)
        myCombo.current(0)
        myCombo.bind("<<ComboboxSelected>>", comboed)
        myCombo.pack()

        zipf_button = ttk.Button(self, text ="Zipf distribution", width=50,
                            command = lambda: plotZip(myCombo.get(), 0)).pack()
        zipfFiltered_button = ttk.Button(self, text ="Zipf filtered",width=50,
                            command = lambda: plotZip(myCombo.get(), 1)).pack()
        histogram_button = ttk.Button(self, text ="Histogram of 20 most frequent words", width=50,
                            command = lambda: plotHisto(myCombo.get())).pack()
        Linear_button = ttk.Button(self, text ="Fit linear regression", width=50,
                            command = lambda: fitZipCurve(myCombo.get())).pack()
        categories_button = ttk.Button(self, text ="Zipf plot and linear regression for the base-10 logarithms", width=50,
                            command = lambda: category(myCombo.get())).pack()
        Exe = ttk.Button(self, text ="Exponential cutoff", width=50,
                            command = lambda: expCutoff(myCombo.get())).pack()
        # numberOfSenses_button = ttk.Button(self, text ="Number of senses", width=50,
        #                     command = lambda: numberSenses(myCombo.get())).pack()
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    def get_page(self,page_class):
        return self.frames[page_class]

app = tkinterApp()
app.mainloop()
