import calendar
import collections
import datetime
import statistics
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

import configs
from components import NavigationButton



class StatisticsPage(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(self.parent)
        self.init_ui()


    def init_ui(self):
        self.setStyleSheet('background-color: none;')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Month selector
        self.month_selector_layout = QHBoxLayout()
        
        self.prev_month_button = NavigationButton('⮜')
        self.prev_month_button.clicked.connect(self.prev_month)

        self.next_month_button = NavigationButton('⮞')
        self.next_month_button.clicked.connect(self.next_month)

        self.month_label = QLabel(self.get_real_time_string())
        self.month_label.setFont(self.parent.body_font(configs.H1_FONT_SIZE))
        self.month_label.setStyleSheet('color: black;')
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.month_label.setMaximumWidth(500)

        self.month_selector_layout.addStretch()
        self.month_selector_layout.addWidget(self.prev_month_button)
        self.month_selector_layout.addWidget(self.month_label)
        self.month_selector_layout.addWidget(self.next_month_button)
        self.month_selector_layout.addStretch()
        self.layout.addLayout(self.month_selector_layout)

        # Greeting label
        self.greeting_label = QLabel(None)
        self.greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greeting_label.setFont(self.parent.body_font(configs.H3_FONT_SIZE))
        self.greeting_label.setStyleSheet('color: black;')
        self.layout.addWidget(self.greeting_label)
        self.layout.addSpacing(12)

        # Heatmap
        self.heatmap_layout = QHBoxLayout()

        self.heatmap_table = QTableWidget()
        self.heatmap_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.heatmap_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.heatmap_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.heatmap_layout.addWidget(self.heatmap_table)

        self.layout.addLayout(self.heatmap_layout)

        # Chart
        self.chart_layout = QHBoxLayout()

        self.chart_view = QChartView()
        self.chart_view.setStyleSheet(f'background-color: {configs.BACKGROUND_COLOR};')
        self.chart_view.setMaximumWidth(800)
        self.chart_layout.addWidget(self.chart_view)

        self.layout.addLayout(self.chart_layout)

        self.layout.addStretch()

        self.refresh()


    def format_time(self, timestamp):
        return timestamp.strftime(configs.STATS_TIME_FORMAT)


    def get_real_time_string(self):
        return self.format_time(datetime.datetime.now())
    

    def get_current_time(self):
        return datetime.datetime.strptime(self.month_label.text(), configs.STATS_TIME_FORMAT)


    def prev_month(self):
        cur_time = self.get_current_time()
        prev_month = cur_time - datetime.timedelta(days=1)
        self.month_label.setText(self.format_time(prev_month))
        self.refresh()


    def next_month(self):
        cur_time = self.get_current_time()
        next_month = cur_time + datetime.timedelta(days=31)
        self.month_label.setText(self.format_time(next_month))
        self.refresh()


    def refresh(self):
        self.check_month_buttons()
        self.update_data()
        self.greeting_label.setText(self.get_encouragement())
        self.update_heatmap()
        self.update_barchart()


    def check_month_buttons(self):
        # Disable next month button if it is the current month
        cur_time = self.get_current_time()
        real_time = datetime.datetime.now()
        if real_time.month == cur_time.month and real_time.year == cur_time.year:
            self.next_month_button.setEnabled(False)
        else:
            self.next_month_button.setEnabled(True)


    def update_data(self):
        cur_time = self.get_current_time()
        self.monthly_data = self.parent.mood_manager.get_monthly_history(cur_time.month, cur_time.year)


    def get_encouragement(self):
        monthly_moods = [entry.mood for entry in self.monthly_data]
        if len(monthly_moods) == 0:
            return configs.ENCOURAGEMENTS['Empty']
        return configs.ENCOURAGEMENTS[statistics.mode(monthly_moods)]


    def update_heatmap(self):
        cur_time = self.get_current_time()
        num_days = calendar.monthrange(cur_time.year, cur_time.month)[1]

        self.heatmap_table.setRowCount(len(configs.MOODS))
        self.heatmap_table.setColumnCount(num_days)

        # Horizontal labels
        self.heatmap_table.setHorizontalHeaderLabels([str(i+1) for i in range(num_days)])
        self.heatmap_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.heatmap_table.horizontalHeader().setMinimumSectionSize(0)
        self.heatmap_table.horizontalHeader().setDefaultSectionSize(33)
        self.heatmap_table.horizontalHeader().setFont(self.parent.body_font(configs.BODY_FONT_SIZE))

        # Vertical labels
        self.heatmap_table.setVerticalHeaderLabels(configs.MOODS)
        self.heatmap_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.heatmap_table.verticalHeader().setDefaultSectionSize(33)
        self.heatmap_table.verticalHeader().setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        self.heatmap_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignRight)

        # General
        self.heatmap_table.setShowGrid(False)
        self.heatmap_table.setStyleSheet(f'''
            color: black;
            background-color: {configs.BACKGROUND_COLOR};
        ''')

        # Get mood counts for each day
        mood_count = {mood: {} for mood in configs.MOODS}
        for entry in self.monthly_data:
            entry_day = datetime.datetime.strptime(entry.timestamp, configs.FILE_TIME_FORMAT)
            mood_count[entry.mood][entry_day.day] = mood_count[entry.mood].get(entry_day.day, 0) + 1

        for (row, mood) in enumerate(configs.MOODS):
            for col in range(num_days):
                num_entries = mood_count[mood].get(col + 1, 0)
                cell = QTableWidgetItem()
                if num_entries == 0:
                    cell.setBackground(configs.MOOD_COLORS[mood][0])
                elif num_entries == 1:
                    cell.setBackground(configs.MOOD_COLORS[mood][1])
                else:
                    cell.setBackground(configs.MOOD_COLORS[mood][2])
                self.heatmap_table.setItem(row, col, cell)

        # Recalculate the table width and height
        total_width = configs.TABLE_PADDING + self.heatmap_table.verticalHeader().width()
        for column in range(self.heatmap_table.columnCount()):
            total_width += self.heatmap_table.columnWidth(column)

        total_height = configs.TABLE_PADDING + self.heatmap_table.horizontalHeader().height()
        for row in range(self.heatmap_table.rowCount()):
            total_height += self.heatmap_table.rowHeight(row)

        self.heatmap_table.setFixedSize(total_width, total_height)
    

    def update_barchart(self):
        # Get number of entries for each mood
        monthly_moods = [entry.mood for entry in self.monthly_data]
        mood_counter = collections.Counter(monthly_moods)
        num_entries = [mood_counter[mood] for mood in configs.MOODS]

        # Make bar chart
        series = QBarSeries()
        bar_set = QBarSet('Moods')
        bar_set.append(num_entries)
        bar_set.setBorderColor(configs.DARK_GRAY_QCOLOR)
        bar_set.setColor(configs.MEDIUM_COLOR_1_QCOLOR)
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(False)
        chart.setBackgroundBrush(QBrush(QColor('transparent')))

        axisX = QBarCategoryAxis()
        axisX.append(configs.MOODS)
        axisX.setLabelsFont(self.parent.body_font(configs.BODY_FONT_SIZE))

        bound = max(num_entries) + 1
        # Make bound a multiple of tick count
        bound += (configs.NONZERO_TICK_COUNT - bound) % configs.NONZERO_TICK_COUNT

        axisY = QValueAxis()
        axisY.setRange(0, bound)
        axisY.setTickType(QValueAxis.TickType.TicksFixed)
        axisY.setTickCount(configs.NONZERO_TICK_COUNT + 1)
        axisY.setLabelFormat('%d')
        axisY.setLabelsFont(self.parent.body_font(configs.BODY_FONT_SIZE))

        pen = QPen(configs.DARK_GRAY_QCOLOR)
        axisX.setLinePen(pen)
        axisX.setGridLinePen(pen)
        axisY.setLinePen(pen)
        axisY.setGridLinePen(pen)

        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

        self.chart_view.setChart(chart)
