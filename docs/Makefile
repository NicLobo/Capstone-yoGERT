# Makefile
# TODO: Missing artifacts should be added to this file
.PHONY:	SRS

all:	SRS MG MIS PS VnVP VnVR DevP HazA Refl UGde

SRS:
	cd SRS && make && cd ..

MG:
	cd Design/MG && make && cd ../..

MIS:
	cd Design/MIS && make && cd ../..

PS:
	cd ProblemStatementAndGoals && make && cd ..

VnVP:
	cd VnVPlan && make && cd ../..

VnVR:
	cd VnVReport && make && cd ../..
	
DevP:
	cd DevelopmentPlan && make && cd ../..
	
HazA:
	cd HazardAnalysis && make && cd ../..
	
Refl:
	cd Reflection && make && cd ../..
	
UGde:
	cd UserGuide && make && cd ../..

clean:	cleanSRS cleanMG cleanMIS cleanPS cleanVnVP cleanVnVR cleanDevP cleanHazA cleanRefl cleanUGde

cleanPS:
	cd ProblemStatementAndGoals && make clean && cd ..

cleanSRS:
	cd SRS && make clean && cd ..

cleanMG:
	cd Design/MG && make clean && cd ..

cleanMIS:
	cd Design/MIS && make clean && cd ..

cleanVnVP:
	cd VnVPlan && make clean && cd ..

cleanVnVR:
	cd VnVReport && make clean && cd ..
	
cleanDevP:
	cd DevelopmentPlan && make clean && cd ..
	
cleanHazA:
	cd HazardAnalysis && make clean && cd ..
	
cleanRefl:
	cd Reflection && make clean && cd ..
	
cleanUGde:
	cd UserGuide && make clean && cd ..
