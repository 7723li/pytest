CREATE TABLE "AgeType" (
"ID" INTEGER,
"Num" TEXT,
"Type" TEXT NOT NULL,
PRIMARY KEY ("Type") 
);

CREATE TABLE "Auditor" (
"ID" INTEGER,
"Num" INTEGER,
"Name" TEXT,
PRIMARY KEY ("ID") 
);

CREATE TABLE "DepName" (
"ID" INTEGER,
"Name" TEXT NOT NULL,
"Num" INTEGER,
PRIMARY KEY ("Name") 
);

CREATE TABLE "Doctor" (
"ID" INTEGER,
"Num" INTEGER,
"Name" TEXT,
"Auditor" TEXT,
"EmployeeID" TEXT,
PRIMARY KEY ("ID") 
);

CREATE TABLE "gem_act_table" (
"PName" TEXT(32),
"Sex" TEXT(16),
"Age" INTEGER,
"AgeType" TEXT(16),
"PID" TEXT(32) NOT NULL,
"Depart" TEXT(32),
"BedNo" TEXT(32),
"DiagNose" TEXT(128),
"BldType" TEXT(32),
"ACT" TEXT(32),
"PrintTime" INTEGER,
"CreatTime" INTEGER,
PRIMARY KEY ("PID") 
);

CREATE TABLE "gem_age_type_table" (
"AgeTypeNo" TEXT(16),
"AgeType" TEXT(16),
PRIMARY KEY ("AgeTypeNo") 
);

CREATE TABLE "gem_auditor_table" (
"AudiNo" TEXT(16),
"AudiName" TEXT(32),
PRIMARY KEY ("AudiNo") 
);

CREATE TABLE "gem_blood_type_table" (
"BldTypeNo" TEXT(16) NOT NULL,
"BldType" TEXT(32),
PRIMARY KEY ("BldTypeNo") 
);

CREATE TABLE "gem_department_table" (
"DepartNo" TEXT(16),
"DepartName" TEXT(64),
PRIMARY KEY ("DepartNo") 
);

CREATE TABLE "gem_diagnose_table" (
"DiagNo" TEXT(16),
"DiagName" TEXT(128),
PRIMARY KEY ("DiagNo") 
);

CREATE TABLE "gem_doctor_table" (
"DocNo" TEXT(16),
"DocName" TEXT(32),
"EleName" TEXT(64),
PRIMARY KEY ("DocNo") 
);

CREATE TABLE "gem_iqm_data_table" (
"Device" TEXT,
"Year" TEXT,
"Month" TEXT,
"Item" TEXT,
"Unit" TEXT,
"SN" TEXT,
"Target" TEXT,
"Material" TEXT,
"Mean" TEXT,
"Low" TEXT,
"High" TEXT,
"Precision" TEXT,
"Interval" TEXT,
"time" INTEGER,
"lowValue" TEXT,
"highValue" TEXT,
"meanValue" TEXT,
"stime" TEXT
);

CREATE TABLE "gem_iqmitem_data_table" (
"itemname" TEXT NOT NULL,
PRIMARY KEY ("itemname") 
);

CREATE TABLE "gem_login_record_table" (
"UserName" TEXT(32),
"LogTime" INTEGER NOT NULL,
"Level" INTEGER,
PRIMARY KEY ("LogTime") 
);

CREATE TABLE "gem_login_table" (
"EmpNo" TEXT(16) NOT NULL,
"PassWord" TEXT(32) NOT NULL,
"CHName" TEXT(32),
"Level" INTEGER,
PRIMARY KEY ("EmpNo") 
);

CREATE TABLE "gem_operator_table" (
"OperaNo" TEXT(16),
"OperaName" TEXT(32),
PRIMARY KEY ("OperaNo") 
);

CREATE TABLE "gem_pinfo_table" (
"PName" TEXT(32),
"Sex" TEXT(16),
"Age" INTEGER,
"AgeType" TEXT(16),
"PID" TEXT(32),
PRIMARY KEY ("PID") 
);

CREATE TABLE "gem_prepinfo_table" (
"PName" TEXT(32),
"PSex" TEXT(16),
"PAge" INTEGER,
"PAgeType" TEXT(16),
"PID" TEXT(32) NOT NULL,
"Depart" TEXT(64),
"BedNo" TEXT(32),
"Diagnose" TEXT(128),
"Doctor" TEXT(32),
"Operator" TEXT(32),
"Auditor" TEXT(32),
PRIMARY KEY ("PID") 
);

CREATE TABLE "gem_qc_cartinfo_table" (
"Instrument" TEXT(64),
"ManuFact" TEXT(64),
"BatchNo" TEXT(32) NOT NULL,
"Qc_Level" INTEGER NOT NULL,
"UseTime" INTEGER,
"Source" TEXT(64),
"TestWay" TEXT(64),
"WaveLen" INTEGER,
"SampNo" TEXT(32),
"OverTime" INTEGER,
"Describe" TEXT(64),
PRIMARY KEY ("BatchNo", "Qc_Level") 
);

CREATE TABLE "gem_qc_cartvalue_table" (
"BatchNo" TEXT(32) NOT NULL,
"Qc_Level" INTEGER NOT NULL,
"itemName" TEXT(16) NOT NULL,
"itemUnit" TEXT(16),
"itemX" TEXT(32),
"itemSD" TEXT(32),
"itemCV" TEXT(32),
PRIMARY KEY ("BatchNo", "Qc_Level", "itemName") 
);

CREATE TABLE "gem_qc_examinfo_table" (
"cartNo" TEXT(32) NOT NULL,
"BatchNo" TEXT(32) NOT NULL,
"ExamTime" INTEGER NOT NULL,
"Qc_Level" INTEGER,
"pH" TEXT(32),
"pCO2" TEXT(32),
"pO2" TEXT(32),
"Na" TEXT(32),
"K" TEXT(32),
"Ca" TEXT(32),
"Glu" TEXT(32),
"Lac" TEXT(32),
"Hct" TEXT(32),
"THb" TEXT(32),
"HHb" TEXT(32),
"MetHb" TEXT(32),
"O2Hb" TEXT(32),
"COHb" TEXT(32),
"SO2" TEXT(32),
"pHT" TEXT(32),
"pO2T" TEXT(32),
"pCO2T" TEXT(32),
"TCO2" TEXT(32),
"HCO3" TEXT(32),
"HCO3std" TEXT(32),
"BEecf" TEXT(32),
"BEB" TEXT(32),
"OI" TEXT(32),
"RI" TEXT(32),
"SO2C" TEXT(32),
"CaO2" TEXT(32),
"pAO2" TEXT(32),
"AaDO2" TEXT(32),
"Cl" TEXT(32),
"Ca74" TEXT(32),
"Ag" TEXT(32),
"TBIL" TEXT(32),
PRIMARY KEY ("ExamTime") 
);

CREATE TABLE "gem_qc_preinput_table" (
"Pid" TEXT(32) NOT NULL,
"cartNo" TEXT(32),
"BatchNo" TEXT(32),
"Qc_Level" INTEGER,
PRIMARY KEY ("Pid") 
);

CREATE TABLE "gem_sample_data_table" (
"ProId" TEXT(32),
"IsRead" TEXT(16),
"ExamTime" INTEGER,
"TranferTime" INTEGER,
"Pid" TEXT(32),
"BldType" TEXT(32),
"Depart" TEXT(32),
"BedNo" TEXT(32),
"ExamTimeStd" INTEGER NOT NULL,
"Doctor" TEXT(16),
"Auditor" TEXT(16),
"Operator" TEXT(16),
"Diagnose" TEXT(16),
"Remark" TEXT(16),
"IsPrint" TEXT(16),
"IsChange" TEXT(16),
"EquipSn" TEXT(32),
"CartSn" TEXT(32),
"pH" TEXT(32),
"pCO2" TEXT(32),
"pO2" TEXT(32),
"Na" TEXT(32),
"K" TEXT(32),
"Ca" TEXT(32),
"Glu" TEXT(32),
"Lac" TEXT(32),
"Hct" TEXT(32),
"THb" TEXT(32),
"HHb" TEXT(32),
"MetHb" TEXT(32),
"O2Hb" TEXT(32),
"COHb" TEXT(32),
"SO2" TEXT(32),
"TCO2" TEXT(32),
"BEecf" TEXT(32),
"tHbc" TEXT(32),
"BEB" TEXT(32),
"Ca74" TEXT(32),
"AG" TEXT(32),
"PFRatio" TEXT(32),
"pAO2" TEXT(32),
"CaO2" TEXT(32),
"CvO2" TEXT(32),
"CcO2" TEXT(32),
"P50" TEXT(32),
"O2cap" TEXT(32),
"O2ct" TEXT(32),
"OI" TEXT(32),
"pHT" TEXT(32),
"pCO2T" TEXT(32),
"pO2T" TEXT(32),
"SO2c" TEXT(32),
"HCO3c" TEXT(32),
"HCO3" TEXT(32),
"HCO3std" TEXT(32),
"AaDO2" TEXT(32),
"paO2pAO2" TEXT(32),
"RI" TEXT(32),
"avDO2" TEXT(32),
"QspQtest" TEXT(32),
"QspQt" TEXT(32),
"Hctc" TEXT(32),
"Temp" TEXT(32),
"BP" TEXT(32),
"AllensTest" TEXT(32),
"Mode1" TEXT(32),
"Mode2" TEXT(32),
"O2Device1" TEXT(32),
"O2Device2" TEXT(32),
"O2" TEXT(32),
"FIO2" TEXT(32),
"MechVT" TEXT(32),
"SpontVT" TEXT(32),
"SetMinuteVol" TEXT(32),
"TotalMinuteVol" TEXT(32),
"MechRatebpm" TEXT(32),
"MechRateHz" TEXT(32),
"SpontRatebpm" TEXT(32),
"SpontRateHz" TEXT(32),
"PIP" TEXT(32),
"MAP" TEXT(32),
"Itimesec" TEXT(32),
"Itime" TEXT(32),
"PEEP" TEXT(32),
"CPAP" TEXT(32),
"BIPAPI" TEXT(32),
"BIPAPE" TEXT(32),
"PS" TEXT(32),
"PC" TEXT(32),
"PulseOX" TEXT(32),
"Flow" TEXT(32),
"Amplitude" TEXT(32),
"DeltaP" TEXT(32),
"HighPEEP" TEXT(32),
"LowPEEP" TEXT(32),
"IPAP" TEXT(32),
"EPAP" TEXT(32),
"ASV" TEXT(32),
"PAV" TEXT(32),
"NitricOxide" TEXT(32),
"Etime" TEXT(32),
"FetHb" TEXT(32),
"APTTP" TEXT(32),
"PTINR" TEXT(32),
"ACTLR" TEXT(32),
"PTP" TEXT(32),
"ACT" TEXT(32),
"PeakPress" TEXT(32),
"VT" TEXT(32),
"VIPAPE" TEXT(32),
"Cl" TEXT(32),
"tBili" TEXT(32),
PRIMARY KEY ("ExamTimeStd") 
);

CREATE TABLE "Look" (
"ID" INTEGER,
"Num" INTEGER,
"Name" TEXT NOT NULL,
PRIMARY KEY ("Name") 
);

CREATE TABLE "Operator" (
"ID" INTEGER,
"Num" INTEGER,
"Name" TEXT,
PRIMARY KEY ("ID") 
);

CREATE TABLE "PInfo" (
"编号" INTEGER,
"PAge" TEXT,
"PID" TEXT NOT NULL,
"PName" TEXT,
"PAge1" TEXT,
"PAgeType" TEXT,
"PSex" TEXT,
"POther" TEXT,
"PBrthdy" TEXT,
"ACT" TEXT,
"DateOfBirth" TEXT,
PRIMARY KEY ("PID") 
);

CREATE TABLE "ptable" (
"ID" INTEGER,
"ProId" TEXT,
"PCNum" TEXT,
"PHNum" TEXT,
"PbbNum" TEXT,
"PCS" TEXT,
"pH" TEXT,
"pO2" TEXT,
"pCO2" TEXT,
"pHT" TEXT,
"pO2T" TEXT,
"pCO2T" TEXT,
"TCO2" TEXT,
"BEecf" TEXT,
"BEB" TEXT,
"HCO3" TEXT,
"HCO3std" TEXT,
"AaDO2" TEXT,
"K" TEXT,
"Na" TEXT,
"Ca" TEXT,
"Glu" TEXT,
"Lac" TEXT,
"Hct" TEXT,
"SO2c" TEXT,
"FiO2" TEXT,
"THbc" TEXT,
"Temp" TEXT,
"Ca74" TEXT,
"THb" TEXT,
"P50" TEXT,
"O2ct" TEXT,
"O2cap" TEXT,
"pAO2" TEXT,
"paO2pAO2" TEXT,
"RI" TEXT,
"CaO2" TEXT,
"CvO2" TEXT,
"CcO2" TEXT,
"avDO2" TEXT,
"QspQt" TEXT,
"REDATA" TEXT,
"PRIDATA" TEXT,
"Other3" TEXT,
"Other4" TEXT,
"Other5" TEXT,
"Other6" TEXT,
"Printer" TEXT,
"InfoPrinter" INTEGER,
"Pid" TEXT,
"O2Hb" TEXT,
"COHb" TEXT,
"MetHb" TEXT,
"HHb" TEXT,
"SO2" TEXT,
"O2" TEXT,
"bloodsam" TEXT,
"FetHb" TEXT,
"APTTP" TEXT,
"PTINR" TEXT,
"ACTLR" TEXT,
"PTP" TEXT,
"ACT" TEXT,
"REDATEadd" TEXT NOT NULL,
"OI" TEXT,
"CPAP" TEXT,
"PEEP" TEXT,
"IsChange" TEXT,
"BIPAPI" TEXT,
"Itimesec" TEXT,
"PeakPress" TEXT,
"VT" TEXT,
"MechRate" TEXT,
"VIPAPE" TEXT,
"MAP" TEXT,
"Itime" TEXT,
"Mode" TEXT,
"SponRate" TEXT,
"PFRatio" TEXT,
"Auditor" TEXT,
"EquipSn" TEXT,
"CartSn" TEXT,
"TranferTime" TEXT,
"Cl" TEXT,
"Bil" TEXT,
"AnionGap" TEXT,
"QspQtest" TEXT,
"Hctc" TEXT,
"tBili" TEXT,
"AG" TEXT,
"HCO3c" TEXT,
"IPAP" TEXT,
"EPAP" TEXT,
"ASV" TEXT,
"PAV" TEXT,
"NitricOxide" TEXT,
"Etime" TEXT,
"Mode1" TEXT,
"Mode2" TEXT,
"O2Device1" TEXT,
"O2Device2" TEXT,
"MechVT" TEXT,
"SpontVT" TEXT,
"SetMinuteVol" TEXT,
"TotalMinuteVol" TEXT,
"MechRatebpm" TEXT,
"MechRateHz" TEXT,
"SpontRatebpm" TEXT,
"SpontRateHz" TEXT,
"PIP" TEXT,
"BP" TEXT,
"AllensTest" TEXT,
"BIPAPE" TEXT,
"PS" TEXT,
"PC" TEXT,
"PulseOx" TEXT,
"Flow" TEXT,
"Amplitude" TEXT,
"DeltaP" TEXT,
"HighPEEP" TEXT,
"LowPEEP" TEXT,
"MOSM" TEXT,
PRIMARY KEY ("REDATEadd") 
);

