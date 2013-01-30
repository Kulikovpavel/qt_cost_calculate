#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import OrderedDict
from PySide.QtCore import *
from PySide.QtGui import *



PROPERTIES = u"""Стоимость,
Ср.срок службы,
Стоимость ТОиР 1 судна""".split(',')

WAY_PROP = u"""Макс. Пасс. При тарифе,
Суточный объем перевозок,
Объем перевозок в месяц,
Время работы,
Время рейса,
Выполнено рейсов,
Время оборота,
Количество причалов,
Скорость сообщения,
Эксплуатационная скорость,
Коэффициент скорости,
Время подхода/отхода,
Время простоя на остановке,
Время простоя на конечном пункте,
Протяженность маршрута,
Пробег одного  судна за смену,
Пассажировместимость,
Коэффициент использования вместимости,
Интервал движения,
Количество рабочих дней в месяц,
Количество судов,
Тариф перевозки""".split(",")

WORKER_PROP = u"""Должность,Численность,Размер з/п руб,Всего з/платы""".split(',')

class Vehicle:
    def __init__(self):

        self.properties =OrderedDict([(x,1) for x in PROPERTIES])


        self.way = OrderedDict([(x,1) for x in WAY_PROP])


        self.workers = [OrderedDict([(x,1) for x in WORKER_PROP])]

        self.work_sum = 0

    def calculate(self,form):
        for i,field in enumerate(form.property_inputs):
            self.properties[self.way.keys()[i]] = field.value()
        for i,field in enumerate(form.way_inputs):
            self.way[self.way.keys()[i]] = field.value()



vehicle = 0
class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.layout = QGridLayout()
        self.vehicle = Vehicle()

#                properties
        self.properties_formLayout = QFormLayout()
        self.layout.addLayout(self.properties_formLayout,0,0)
        self.property_inputs = []
        for i,field in enumerate(self.vehicle.properties.keys()):
            spinbox = QDoubleSpinBox()
            spinbox.setMaximum(1e9)
            spinbox.setValue(self.vehicle.properties[field])

            self.properties_formLayout.addRow(field, spinbox)
            self.property_inputs.append(spinbox)
        self.button = QPushButton("Show Greetings")
        self.properties_formLayout.addRow(self.tr(""),self.button)

#                 way
        self.way_formLayout = QFormLayout()
        self.layout.addLayout(self.way_formLayout,1,0)
        self.way_inputs = []
        for i,field in enumerate(self.vehicle.way.keys()):
            spinbox = QDoubleSpinBox()
            spinbox.setMaximum(1e9)
            spinbox.setValue(self.vehicle.way[field])

            self.way_formLayout.addRow(field, spinbox)
            self.way_inputs.append(spinbox)
        self.button = QPushButton("Show Greetings")
        self.way_formLayout.addRow(self.tr(""),self.button)

#                 workers
        self.work_sum = QSpinBox()  # sum for all workers table
        self.work_sum.setMaximum(1e9)
        self.work_sum.value = 0
        self.workers_layout = QVBoxLayout()
        self.workers_table = QTableWidget(0,4)
        self.workers_table.setMinimumWidth(450)
        self.workers_table.setHorizontalHeaderLabels(WORKER_PROP)

        self.workers_layout.addWidget(self.workers_table)
        self.layout.addLayout(self.workers_layout,0,1)
        self.workers_inputs = []
        self.table_button_add = QPushButton(u"Добавить строку")
        self.table_button_delete = QPushButton(u"Удалить строку")

        self.workers_layout.addWidget(self.table_button_add)
        self.workers_layout.addWidget(self.table_button_delete)
        self.table_button_add.clicked.connect(self.table_row_add)
        self.table_button_delete.clicked.connect(self.table_row_delete)
        self.workers_table.itemChanged.connect(self.table_changed)
        self.work_sum.valueChanged.connect(self.work_sum_changed)

        form_sum = QFormLayout()
        form_sum.addRow(u'Сумма', self.work_sum)
        self.workers_layout.addLayout(form_sum)

        self.start_button = QPushButton(u"Расчет")
        self.layout.addWidget( self.start_button, 1, 1)
        self.start_button.clicked.connect(self.calculate)




        self.button.clicked.connect(self.greetings)
        self.setLayout(self.layout)
    def get_way_input(self, name):
        if isinstance(name, int):
            return self.way_inputs[name-5].value()
        else:
            return self.way_inputs[WAY_PROP.index(name)].value()
    def set_way_input(self, name, val):
        if isinstance(name, int):
            return self.way_inputs[name-5].setValue(val)
        else:
            return self.way_inputs[WAY_PROP.index(name)].setValue(val)




    def calculate(self):

        g = self.get_way_input
        self.set_way_input(7, g(6)*g(24))
        self.set_way_input(9, (g(19)/g(13)*60+g(12)*(g(16)+g(17))+g(18))/60)  # ((D19/D13)*60+D12*(D16+D17)+D18)/60

        self.set_way_input(10, g(8)/g(9))
        self.set_way_input(11, 2*g(9))

        self.set_way_input(25, g(5)*g(11)/g(21))  #  D5*D11/D21
        self.set_way_input(23, g(11)/g(25)*60)  #  =(D11/D25)*60
        self.vehicle.calculate(self)
    # Greets the user
    def greetings(self):
        for elem in self.inputs:
            print elem.text()
    def table_row_add(self):
        row = self.workers_table.rowCount()
        self.workers_table.insertRow(row)
    def table_row_delete(self):
        self.workers_table.removeRow(self.workers_table.currentRow())
    def work_sum_changed(self):
        self.vehicle.work_sum = self.work_sum.value
    def table_changed(self):
        try:
            self.workers_table.blockSignals(True)
            work_sum = 0
            for i in range(self.workers_table.rowCount()):
    #            self.workers_table.setCellWidget(i,3,)
                self.workers_table.setItem(i,3,  QTableWidgetItem(str(int(self.workers_table.item(i,1).text()) *\
                                                 int(self.workers_table.item(i,2).text()) )))

                work_sum += int(self.workers_table.item(i,3).text())


            self.work_sum.setValue(work_sum)
            self.workers_table.blockSignals(False)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print "Unexpected error:", sys.exc_info()[1]
            self.workers_table.blockSignals(False)




if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())