'''
Created on Apr 28, 2014

@author: perk
test commit
'''

from pylab import *

class Deal(object):
    
    def __init__(self, name, price, propTaxRate, closingCosts, insuranceMo,
                 propertyManagerMo, rentMo, appreciationRate, assessmentsMo, downPayment, loanRate, term, specialMo, emptyMonths):
        
        self.name = name
        self.price = price
        self.propTaxRate = propTaxRate/100.0
        self.closingCosts = closingCosts 
        self.insuranceMo = insuranceMo
        self.propertyManagerMo = propertyManagerMo/100.0*rentMo
        self.rentMo = rentMo
        self.appreciationRate = appreciationRate
        self.assessmentsMo = assessmentsMo
        self.downPayment = downPayment/100.0
        self.loanRate = loanRate/100.0/12.0
        self.term = term
        self.specialMo = specialMo
        self.emptyMonths = emptyMonths
        
        self.CalculateROI()
        
    def CalculateROI(self):
        self.cost = self.price + self.closingCosts
        self.loanAmt = self.cost - self.downPayment*self.cost
        self.numberOfPayments = self.term*12
        self.mortgagePaymentMo = self.loanAmt * self.loanRate*pow(self.loanRate+1, self.numberOfPayments) / (pow(self.loanRate+1, self.numberOfPayments) - 1)
        self.paymentMo = self.mortgagePaymentMo + self.assessmentsMo + self.price*self.propTaxRate/12.0 + self.insuranceMo + self.propertyManagerMo + self.specialMo
        self.incomeMo = self.rentMo - self.paymentMo - self.rentMo*self.emptyMonths/12.0
        self.roi = self.incomeMo * 12 / (self.downPayment*self.cost) * 100.0
        self.roiAdjusted = self.roi + self.appreciationRate
        return self.roi
        
    def __str__(self):

        out = 'ROI summary\n------------------------------------\n'
        out += 'Monthly payment:  \t%.2f\n' % (self.paymentMo)
        out += '\tMortgage:  \t%.2f\n' % (self.mortgagePaymentMo)
        out += '\tAssessments:  \t%.2f\n' % (self.assessmentsMo)
        out += '\tProperty tax:  \t%.2f\n' % (self.propTaxRate*self.price/12.0)
        out += '\tInsurance:  \t%.2f\n' % (self.insuranceMo)
        out += '\tProperty mgmt:\t%.2f\n' % (self.propertyManagerMo)
        out += '\tSpecial circ:\t%.2f\n' % (self.specialMo)
        out += 'Monthly income:   \t%.2f\n' % (self.incomeMo)
        out += 'ROI               \t%.2f\n' % (self.roi)
        out += 'ROI adjusted      \t%.2f\n' % (self.roiAdjusted)
        out += '\nInput summary\n------------------------------------\n'
        out += 'Price:         \t%.2f\n' % (self.price)
        out += 'Prop tax rate: \t%.2f\n' % (self.propTaxRate*100.0)
        out += 'Closing costs: \t%.2f\n' % (self.closingCosts)
        out += 'Insurance:     \t%.2f\n' % (self.insuranceMo)
        out += 'Prop Mgmt:     \t%.2f\n' % (self.propertyManagerMo)
        out += 'Rent:          \t%.2f\n' % (self.rentMo)
        out += 'Appreciation:  \t%.2f\n' % (self.appreciationRate*100.0)
        out += 'Assessments:   \t%.2f\n' % (self.assessmentsMo)
        out += 'Down payment:  \t%.2f\n' % (self.downPayment*100.0)
        out += 'Loan rate:     \t%.2f\n' % (self.loanRate*100.0*12.0)
        out += 'Loan term:     \t%.2f\n' % (self.term)
        out += 'Special circ:  \t%.2f\n' % (self.specialMo)
        out += 'Empty Months:  \t%.2f\n' % (self.emptyMonths)
         
        return out
        
    def ROIvsDownPayment(self, downPayments):
        
        cache = self.downPayment
        roiList = list()
        
        for dp in downPayments: 
            self.downPayment = dp/100.0
            roiList.append(self.CalculateROI())
            
        self.downPayment = cache
        
        figure()
        plot(downPayments, roiList)
        plot([downPayments[0], downPayments[-1]], [0, 0])
        xlabel('down payment %')
        ylabel('ROI %')
        grid(True)
        savefig('roi_vs_downPayment.png')        
        
    def ROIvsLoanRate(self, rates):
        cache = self.loanRate
        roiList = list()
        
        for r in rates: 
            self.loanRate = r/100.0/12.0
            roiList.append(self.CalculateROI())
            
        self.loanRate = cache
        
        figure()
        plot(rates, roiList)
        plot([rates[0], rates[-1]], [0, 0])
        xlabel('loan rate %')
        ylabel('ROI %')
        grid(True)
        savefig('roi_vs_loanRate.png')        
        
    def ROIvsEmptyMonths(self, rates):
        cache = self.emptyMonths
        roiList = list()
        
        for r in rates: 
            self.emptyMonths = r
            roiList.append(self.CalculateROI())
            
        self.emptyMonths = cache
        
        figure()
        plot(rates, roiList)
        plot([rates[0], rates[-1]], [0, 0])
        xlabel('# of empty months per year')
        ylabel('ROI %')
        grid(True)
        savefig('roi_vs_emptyMonths.png')        
        
    def ROIoverTime(self, numYears):
        
        figure(figsize=(8.5,11.0))
        lines = list()
        legStrs = list()
        
        for appRate in arange(-2.0, 4.0, 1.0):

            outFile = open('%s_roi_vs_time_%.2f.txt' % (self.name, appRate),'w')
            outFile.write('year\tcapital\tdownP\tnewValue\tappValue\tcashFlow\tmo.pay\troi\n')
            income = 0.0
            payments = 0.0
            revenue = 0.0
            incomeList = list()
            paymentList = list()
            netList = [-self.downPayment*self.cost]
            roiList = list()
            capitalList = list()
            years = range(1,numYears+1)
            for y in years:
                
                # calculate new home value
                newValue = self.price*pow(appRate/100.0 + 1.0, y)
                appValue = newValue - self.price
                
                # assume rent increases at appRate
                newRent = self.rentMo*pow(appRate/100.0 + 1.0, y-1)
                
                # increase monthly payments
                newTax = newValue*self.propTaxRate
                moIncrease = newTax - self.price*self.propTaxRate
                
                incomeList.append((12-self.emptyMonths)*newRent)
                payment = self.paymentMo*12 + moIncrease
                if y > self.term : payment -= self.mortgagePaymentMo*12
                paymentList.append(payment)
                netList.append(incomeList[-1] - paymentList[-1])
                
                income += incomeList[-1]
                payments += paymentList[-1]
                roi = 0.0
                
                revenueReturn = 0.0*revenue
                
                roi = max(-.2, pow( (revenueReturn + income-payments + self.downPayment*self.cost - self.closingCosts + appValue) / (self.downPayment*self.cost), 1.0/y) - 1.0)
                roiList.append(roi*100.0)
                
                
                revenue += incomeList[-1] - paymentList[-1] + revenueReturn
                
                capitalList.append(revenue)
                
                outFile.write('%d\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n' % \
                              (y, (income-payments + self.downPayment*self.cost - self.closingCosts + appValue), (self.downPayment*self.cost), newValue, appValue, revenue, payment, roi))
            subplot(2,1,1)
            l, = plot(years, roiList)
            lines.append(l)
            legStrs.append('%.1f' % (appRate))
            
            subplot(2,1,2)
            plot(years, capitalList)
            outFile.close()
            
            
        xlabel('year')
        ylabel('revenue')
        grid(True)
        legend(lines, legStrs, loc = 2)
        plot([years[0], years[-1]], [self.downPayment*self.cost, self.downPayment*self.cost],'k')
        subplot(2,1,1)
        plot([years[0], years[-1]], [0, 0],'k')
        plot([years[0], years[-1]], [10, 10],'k')
        ylabel('ROI %')
        title('App. rate analysis, emptyMonths = %.1f' % (self.emptyMonths))
        savefig('roi_vs_time.png')   
        show()             


if __name__ == '__main__':
    
    perkCondo = Deal('perkCondo', 349000.00, 1.54, 8375, 50.0, 9.0, 2700.0, 0.0, 515.30, 21.872, 2.875, 30, 100.0, 1)
   
    print(perkCondo)
    
    #perkCondo.ROIvsDownPayment(range(10,51,1))
    #perkCondo.ROIvsLoanRate(arange(2.5,5.5,0.1))
    #perkCondo.ROIvsEmptyMonths(arange(0.0,2.0,0.1))
    perkCondo.ROIoverTime(40)
    
    # lender paid:
    #    1% commission to broker
    #    1570.50 in transfer taxes
    
    # closing costs included 
    #    loan origination fee
    #    required services that you can shop for
    #    association fees
    #    back taxes
    #    additional
    #    credit report
    #    appraisal fees
    
    # title fees included closing fee, owner's title insurance, lender's title insurance, and other
    
    # transfer fees included recording charges (144) and transfer taxes (0.75%)
    

    