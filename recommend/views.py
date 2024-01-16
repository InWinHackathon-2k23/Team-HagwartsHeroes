from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request,'home.html')
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def result(request):
    
    def suggest_investment_sequence(principal, tenure):
        schemes = [
            {"scheme_name": "Savings Account", "Minimum Deposit": 100, "Maximum Deposit": float('inf'), "tenure": None, "rate_of_interest": 0.05},
            {"scheme_name": "Fixed Deposits", "Minimum Deposit": 1000, "Maximum Deposit": float('inf'), "tenure": 5, "rate_of_interest": 0.0775},
            {"scheme_name": "Monthly Income Scheme", "Minimum Deposit": 500, "Maximum Deposit": 900000, "tenure": 3, "rate_of_interest": 0.074},
            {"scheme_name": "National Savings Certificate VIII Issue 2019", "Minimum Deposit": 1000, "Maximum Deposit": 500000, "tenure": 5, "rate_of_interest": 0.077},
        ]
        sorted_schemes = sorted(schemes, key=lambda x: x["rate_of_interest"], reverse=True)

        remaining_principal = principal
        total_returns = 0
        investment_sequence = []
        remaining_tenure=tenure

        for scheme in sorted_schemes:
            if scheme["tenure"] is not None and tenure < scheme["tenure"]:  
                continue  # Skip schemes with tenure greater than investor's tenure

            scheme_tenure = scheme["tenure"] if scheme["tenure"] is not None else tenure

            while remaining_principal >= scheme["Minimum Deposit"]:
                max_investment = min(remaining_principal, scheme["Maximum Deposit"])
                remaining_principal -= max_investment

                investment_sequence.append({
                    "scheme_name": scheme["scheme_name"],
                    "investment_amount": max_investment,
                    "rate_of_interest": scheme["rate_of_interest"]*100,
                    "tenure": scheme_tenure
                })

            # Calculate total returns at the end of scheme's tenure
                total_returns += max_investment * (1 + scheme["rate_of_interest"])**scheme_tenure

        # If there is remaining tenure, invest total returns and remaining principal in Savings Account
            remaining_tenure = remaining_tenure - scheme_tenure
            
            if remaining_tenure > 0:
                savings_account = {
                    "scheme_name": "Savings Account",
                    "investment_amount": total_returns + remaining_principal,
                    "rate_of_interest": 5,
                    "tenure": remaining_tenure
                }
                investment_sequence.append(savings_account)
                remaining_principal = 0
                remaining_tenure=0
                total_returns = total_returns* (1 + 0.05)**remaining_tenure
                
        
        return round(total_returns, 2), investment_sequence
    


    principal=float(request.POST['principal_amount'])
    tenure=float(request.POST['investment_tenure'])
    total_returns,investment_sequence=suggest_investment_sequence(principal, tenure)
    return render(request,"result.html",{'investment_sequence':investment_sequence,'total_returns':total_returns})

