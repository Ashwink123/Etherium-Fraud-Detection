from pydantic import BaseModel

class Transactions_Response(BaseModel):
    Total_ERC20_tnxs : float
    ERC20_uniq_rec_addr : float
    ERC20_uniq_rec_contract_addr :  float
    Time_Diff_between_first_and_last_(Mins) : float
    total_ether_balance : float
    max_value_received : float
    avg_val_received : float
    ERC20_min_val_rec : float
    Unique_Received_From_Addresses : float
    Received_Tnx : float
    min_value_received : float
    Avg_min_between_received_tnx : float
    Avg_min_between_sent_tnx : float
    total_Ether_sent : float
    max_val_sent : float
    Sent_tnx : float
    avg_val_sent :  float
    ERC20_total_Ether_received : float
    Flag : str