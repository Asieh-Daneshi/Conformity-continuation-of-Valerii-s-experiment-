close all
clear
clc
% Asieh Daneshi
% February 21, 2023
%% ========================================================================
% -------------------------------------------------------------------------
Data=readtable('data.csv');
NP=160;     % number of participants
NT=148;     % 10 practice1 + 64 block1 + 10 practice2 + 64 block2
NTT=128;    % only test trials
% Data=reshape(Data,NT,[]);
data_length=size(Data,1);
b1=1;
for a1=11:NT:data_length
    MainBlock1(b1:b1+63,:)=Data(a1:a1+63,:);
    MainBlock2(b1:b1+63,:)=Data(a1+74:a1+74+63,:);
    b1=b1+64;
end

b2=1;
for a2=1:64:size(MainBlock1,1)
    % Participant number
    Data_B1(a2:a2+63,1)=ones(64,1)*b2;
    Data_B2(a2:a2+63,1)=ones(64,1)*b2;
    % Block number (1:block1, 2:block2)
    Data_B1(a2:a2+63,2)=ones(64,1);
    Data_B2(a2:a2+63,2)=ones(64,1)*2;
    % Is catch? (true:1, false:0)
    Data_B1((a2-1)+(find(string(table2array(MainBlock1(a2:a2+63,3)))=='TRUE')),3)=1;
    Data_B2((a2-1)+(find(string(table2array(MainBlock2(a2:a2+63,3)))=='TRUE')),3)=1;
    % column 4: Trial length; column 5: Number of agents;
    Data_B1(a2:a2+63,4:5)=table2array(MainBlock1(a2:a2+63,6:7));
    Data_B2(a2:a2+63,4:5)=table2array(MainBlock2(a2:a2+63,6:7));
    % congruency: 0:IC, 1:C
    Data_B1((a2-1)+(find(string(table2array(MainBlock1(a2:a2+63,8)))=='C')),6)=1;
    Data_B2((a2-1)+(find(string(table2array(MainBlock2(a2:a2+63,8)))=='C')),6)=1;
    % Response time
    Data_B1(a2:a2+63,7)=table2array(MainBlock1(a2:a2+63,9));
    Data_B2(a2:a2+63,7)=table2array(MainBlock2(a2:a2+63,9));
    % Group alignment
    Data_B1((a2-1)+(find(string(table2array(MainBlock1(a2:a2+63,10)))=='F')),8)=1;
    Data_B2((a2-1)+(find(string(table2array(MainBlock2(a2:a2+63,10)))=='F')),8)=1;
    % First Agent response time
    Data_B1(a2:a2+63,9)=table2array(MainBlock1(a2:a2+63,11));
    Data_B2(a2:a2+63,9)=table2array(MainBlock2(a2:a2+63,11));
    % Percentage of orange pixels
    Data_B1((a2-1)+(find(string(table2array(MainBlock1(a2:a2+63,12)))~='NA')),10)=str2double(table2array(MainBlock1((a2-1)+find(string(table2array(MainBlock1(a2:a2+63,12)))~='NA'),12)));
    Data_B2((a2-1)+(find(string(table2array(MainBlock2(a2:a2+63,12)))~='NA')),10)=str2double(table2array(MainBlock2((a2-1)+find(string(table2array(MainBlock2(a2:a2+63,12)))~='NA'),12)));
    Data_B1((a2-1)+(find(string(table2array(MainBlock1(a2:a2+63,12)))=='NA')),10)=0.5;
    Data_B2((a2-1)+(find(string(table2array(MainBlock2(a2:a2+63,12)))=='NA')),10)=0.5;
    % Subject validity
    Data_B1((a2-1)+(find(string(table2array(MainBlock1(a2:a2+63,13)))=='TRUE')),11)=1;
    Data_B2((a2-1)+(find(string(table2array(MainBlock2(a2:a2+63,13)))=='TRUE')),11)=1;
    % Trial validity
    Data_B1((a2-1)+(find(string(table2array(MainBlock1(a2:a2+63,14)))=='TRUE')),12)=1;
    Data_B2((a2-1)+(find(string(table2array(MainBlock2(a2:a2+63,14)))=='TRUE')),12)=1;
    b2=b2+1;
end
    

