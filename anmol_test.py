"""
Minimalist script to test lmlib ETA Planner client against the running Spring Boot server.
"""

from lmlib.eta_calculator import CWEtaPlannerClient


def main():
    print("=== 1. Checking CW ETA Planner Service Health ===")
    client = CWEtaPlannerClient(base_url="http://localhost:8080")
    
    try:
        status = client.check_status()
        print(f"Status response     : {status.get('status')}")
        print(f"Service API Version : {status.get('apiVersion')}\n")
    except Exception as e:
        print(f"Failed to connect to API: {e}")
        return

    print("=== 2. Defining Custom Input Parameters ===")
    input_data = {
        "resetBeforeRun": True,
        "vessels": [
            {
                "id": "VESSEL-ANMOL-01",
                "name": "Anmol Express",
                "capacityWeightTons": 5500.0,
                "maxMonopiles": 4,
                "speedKnots": 14.5,
                "availableFromDay": 0.0,
                "compatibleGrillageTypes": ["Type-A", "Type-B"],
                "operationalCalendar": "24/7",
                "vesselClass": "TClass"
            }
        ],
        "monopiles": [
            {
                "id": "MP-ANMOL-01",
                "weightTons": 1300.0,
                "lengthM": 82.0,
                "grillageType": "Type-A",
                "fabricationYardId": "FAB-01",
                "installationSiteId": "SITE-01",
                "fabricationCompletionDay": 5.0,
                "targetInstallationDay": 90.0,
                "originLogisticsKey": "NordenhamGermany",
                "destinationLogisticsKey": "Argentia",
                "voyageProfile": "DS"
            }
        ]
    }

    print("=== 3. Calling CW ETA Planner Solver API ===")
    results = client.run_solver(input_data=input_data)

    print("\n=== 4. Solver Execution Results ===")
    print(f"Best Solver Used : {results.get('bestSolverName')}")
    print(f"Best Score       : {results.get('bestScore')}")
    
    schedule = results.get("schedule")
    if isinstance(schedule, list):
        print(f"Total Trips Scheduled: {len(schedule)}")
        for i, item in enumerate(schedule, 1):
            print(f"  Item {i}: {item}")
    elif isinstance(schedule, dict):
        trips = schedule.get("trips", [])
        print(f"Total Trips Scheduled: {len(trips)}")
        for i, item in enumerate(trips, 1):
            print(f"  Trip {i}: {item}")
    else:
        print(f"Full Response JSON: {results}")

    print("\n=== 5. Downloading PDF Schedule Report ===")
    try:
        pdf_bytes = client.download_report_pdf(output_filename="anmol_test_report.pdf")
        if pdf_bytes:
            print("Successfully downloaded report as anmol_test_report.pdf")
        else:
            print("PDF report not available (404).")
    except Exception as e:
        print(f"Could not download PDF report: {e}")


if __name__ == "__main__":
    main()
