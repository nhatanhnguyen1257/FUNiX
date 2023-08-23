# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
import os
 

class lastname_firstname_grade_the_exams:

    # đường đẫn tới thư mục lưu file
    path = "D:\ML-Funix\giới thiệu học máy\Assignment\Data Files"  
    
    # số lượng câu trả lời cần có
    max_line = 26
    
    # đáp án các câu hỏi từ 1 tới 26
    answer_key = str("B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D").split(",")
    
    # danh sách lưu điểm số theo mã học sinh
    scores_answer = {}
    
    # số row đáp hợp lệ
    row_ok = 0
    # số row đáp án không hợp lệ
    row_false = 0
    
    
    
    def Input(self):
        self.row_ok = 0
        self.row_false = 0
        # tên của file người dùng nhập vào kiếm tra
        self.nameFile = input('Nhập tên file bạn muốn đọc: ')

        if self.ExistFile(self.nameFile):
            print("Mở thành công file " + self.nameFile + ".txt")
           
            self.ReadFile(nameFile = self.nameFile) 
            
        else:
            print("Không tìm thấy file.")
        return 
    


    def ExistFile(self, nameFile):
        '''
        kiểm tra xem file đó có tồn tại trong thư mục hay không
        '''
        # Đọc toàn bộ file có trong thư mục
        for (root, dirs, file) in os.walk(self.path):
            for f in file:
                if (nameFile + ".txt") in f:
                    return True
                 
        return False
   
    def ReadFile(self, nameFile):
        '''
        Đọc file csv
        '''
        print("\n*********Bắt đầu phân tích*****************\n")
        data = pd.DataFrame(pd.read_csv(self.path +"\\" +nameFile+".txt", on_bad_lines='skip', header=None))
        # self.max_line = data.shape[1]
        print("Tổng số dòng dữ liệu được lưu trữ trong file: " + str(data.shape[0]))
        
        for row in range(data.shape[0]):
            self.IsValidate(rowOfdataFrame=row, dataFrame=data)
            
            
        print("\nSố lượng dòng hợp lệ: " + str(self.row_ok))
        print("Số lượng dòng không hợp lệ: " + str(self.row_false))
        
        print("\n********Kết thúc phân tích************\n")
        
        print("***********Thông kê**************\n")
        self.PrintScores()
        print("\n***********Thông kê hoàn thành**************")
        self.WriteFileScores()
            
        
    def IsValidate(self, rowOfdataFrame, dataFrame):
        '''
        Kiểm tra tính họp lệ của dữ liệu
        
        Phân tích từng dòng và đảm bảo rằng nó là "hợp lệ".
        Một dòng hợp lệ chứa danh sách 26 giá trị được phân tách bằng dấu phẩy
        N# cho một học sinh là mục đầu tiên trên dòng. Nó phải chứa ký tự “N” theo sau là 8 ký tự số.
        
        '''
        lstDataRow = dataFrame.iloc[rowOfdataFrame].tolist();
       
        self.Scores(lstDataRow)
        if (len(lstDataRow) != self.max_line):
            print("Dòng không chứa đủ " + str(self.max_line) + " ký tự: ")
            print(*lstDataRow, sep = ", ")
            self.row_false +=1
            return
        elif len(lstDataRow[0]) != 9:
            print("Dòng định dạng mã sinh viên không đủ số ký tự: ")
            print(*lstDataRow, sep = ", ")
            self.row_false +=1
            return
        elif lstDataRow[0][0] != 'N' :
            print("Dòng định dạng mã sinh viên không đúng định dạng N bắt đầu: ")
            print(*lstDataRow, sep = ", ")
            self.row_false +=1
            return
        elif lstDataRow[0][1::].isdigit() == False:
            print("Dòng định dạng mã sinh viên không phải là số: ")
            print(*lstDataRow, sep = ", ")
            self.row_false +=1
            return
        for col in range(dataFrame.shape[1]):
            # print(dataFrame.iloc[rowOfdataFrame, col])
            if str(dataFrame.iloc[rowOfdataFrame, col]) == '':  
                print("Dòng chứa những có những đáp án trắng")
                print(*lstDataRow, sep = ", ")
                self.row_false +=1
                return
        self.row_ok +=1
        return
    
    def Scores(self,lstAnswers): 
        '''
        Tính điểm của của 1 bài đã lọp tương ứng với mã sinh viên
        
        +4 điểm cho mỗi câu trả lời đúng
        0 điểm cho mỗi câu trả lời bị bỏ qua
        -1 điểm cho mỗi câu trả lời sai
        
        '''
        score = 0
        for index in range(1, len(lstAnswers)):
            if lstAnswers[index] == self.answer_key[index-1]:
                score +=4
            elif lstAnswers[index] != self.answer_key[index-1] and (len(str(lstAnswers[index])) == 1) and score > 0:
                score -= 1
                
        self.scores_answer[lstAnswers[0]] = score
        
    
    def WriteFileScores(self):
        '''
        Ghi điểm dữ liệu điểm vào file txt
        '''
        fileName =  self.nameFile + "_grades.txt"
        print("\nĐang ghi file:  " + fileName)
        with open( fileName,'w') as f:
            for key in self.scores_answer.keys():
                f.write(str(key) + ", " + str( self.scores_answer[key]) + "\n")
        print("Ghi file hoàn thành:  " + fileName)
    
    
    def PrintScores(self):
        '''in điểm'''
        max = 0
        min = 100
        average = 0
        for key in self.scores_answer.keys():
            average += self.scores_answer[key]
            if self.scores_answer[key] > max:
                max = self.scores_answer[key]
            if self.scores_answer[key] < min:
                min = self.scores_answer[key]
        
        average = round(average/len(self.scores_answer),2)
        
        print("Điểm số cao nhất: " + str(max))
        print("Điểm số thấp nhất: " + str(min))
        print("Điểm trung bình: " + str(average))
        print("Miền giá trị của điểm: " +  str(max - min))
        
        # =============================================================================
        #   Giá trị trung vị (Sắp xếp các điểm theo thứ tự tăng dần. Nếu # học sinh là số lẻ, 
        #   bạn có thể lấy giá trị nằm ở giữa của tất cả các điểm (tức là [0, 50, 100] — trung vị là 50). 
        #   Nếu # học sinh là chẵn bạn có thể tính giá trị trung vị bằng cách lấy giá trị trung bình của hai giá trị giữa
        #   (tức là [0, 50, 60, 100] — giá trị trung vị là 55)).
        # =============================================================================
        
        list_values = list(dict(sorted(self.scores_answer.items(), key=lambda item: item[1])).values())
        index = int(len(self.scores_answer) / 2)
        if len(self.scores_answer) % 2 == 0:
            print("Giá trị trung vị: " +  str(round(( float(list_values[index]) + float(list_values[index + 1]))/2)))
        else:
            print("Giá trị trung vị: " +  str( list_values[index + 1]))
            
    
p = lastname_firstname_grade_the_exams()
p.Input()