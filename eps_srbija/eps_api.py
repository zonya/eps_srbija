import requests

BASE_URL = "https://apiportal.eps.rs/api"

def validate_login(email, password):
    res = requests.post(f"{BASE_URL}/account/authenticate",
                        json={"username": email, "password": password, "deviceTypeId": 1})
    return res.status_code == 200

def get_eps_full_data(email, password):
    with requests.Session() as session:
        # 1. Autentifikacija
        login_res = session.post(f"{BASE_URL}/account/authenticate", 
                                 json={"username": email, "password": password, "deviceTypeId": 1})
        if login_res.status_code != 200: 
            return None
        
        token = login_res.json().get("token", {}).get("accessToken")
        session.headers.update({
            "Authorization": f"Bearer {token}", 
            "Accept": "application/json", 
            "Content-Type": "application/json"
        })

        # 2. Ugovori (Saldo i broj ugovora)
        contracts_res = session.get(f"{BASE_URL}/contracts/commercial-contracts")
        contracts_data = contracts_res.json() if contracts_res.status_code == 200 else []
        
        # 3. Upozorenja (Opomene)
        warnings_res = session.get(f"{BASE_URL}/finances/warnings")
        warnings = warnings_res.json() if warnings_res.status_code == 200 else []
        
        # 4. Poruke (Obaveštenja sistema)
        messages_res = session.post(f"{BASE_URL}/administration/messages/search", 
                                    json={"take": 5, "sortColumnName": "sentAt", "sortColumnDirection": "DESC"})
        messages = messages_res.json().get("data", []) if messages_res.status_code == 200 else []

        # 5. Priprema parametara za finansije i potrošnju
        cont_res = session.post(f"{BASE_URL}/contracts/commercial-contracts/search", 
                                json={"take": 1, "sortColumnName": "id", "sortColumnDirection": "DESC"})
        c_id = cont_res.json()["data"][0]["id"]
        
        pod_res = session.post(f"{BASE_URL}/metering/points-of-deliveries/search", 
                               json={"take": 1, "commercialContractId": c_id})
        d_id = pod_res.json()["data"][0]["id"]
        params = {"commercialContractId": c_id, "PointOfDeliveryId": d_id}

        # 6. Poslednji račun
        doc_res = session.post(f"{BASE_URL}/finances/financial-documents/search", 
                               json={"take": 1, "commercialContractId": c_id})
        doc_list = doc_res.json().get("data", [])
        doc_details = {}
        if doc_list:
            doc_id = doc_list[0]["id"]
            doc_details = session.get(f"{BASE_URL}/finances/financial-documents/{doc_id}").json()

        # 7. Potrošnja
        kwh_res = session.get(f"{BASE_URL}/dashboard/consumption-last-twelve-months", params=params)
        rsd_res = session.get(f"{BASE_URL}/dashboard/consumption-amount-last-twelve-months", params=params)

        # Povratni objekat za Home Assistant senzor
        return {
            "status": "OK",
            "finansije": {
                "iznos": doc_details.get("amount", 0.0), 
                "poziv_na_broj": doc_details.get("paymentReference", ""), 
                "rok_dospeca": doc_details.get("dueDate", "")[:10] if doc_details.get("dueDate") else ""
            },
            "status_duga": {
                "balance_amount": contracts_data[0].get("balanceAmount", 0.0) if contracts_data else 0.0, 
                "commercial_contracts_number": contracts_data[0].get("commercialContractsNumber", "") if contracts_data else ""
            },
            "opomene": warnings,
            "poruke": messages,
            "potrosnja_kwh": kwh_res.json() if kwh_res.status_code == 200 else [],
            "potrosnja_rsd": rsd_res.json() if rsd_res.status_code == 200 else []
        }
