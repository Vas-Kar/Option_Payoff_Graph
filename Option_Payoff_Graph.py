### ------------------ Import Libraries ------------------ ###
import streamlit as st
import numpy as np
import pandas as pd

import time
import io #to save the matplotlib chart to a buffer so that we can download it later

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator #? to set y axis only to integers in the bar chart
import plotly.graph_objects as pgo

from PIL import Image

Image.MAX_IMAGE_PIXELS = 500_000_000 #Increase pixel size limit

###! ------------------ Initial Page Configuration ------------------ ###

st.set_page_config(page_title="Option Expiration Payoff", layout="wide")    


st.title(":blue[Option Expiration Payoff Graphs]")

###! ------------------ Linkedin ------------------ ###

st.write("Created by:")
st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 10px;'>
            <img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg' width='20'/>
            <a href='https://www.linkedin.com/in/vasilis-karantzas' target='_blank'>Vasilis Karantzas</a>
        </div>
        """,
        unsafe_allow_html=True
)
st.markdown("""---""")


#! Project Description
with st.expander("ℹ️ Project Description", expanded=False):
    st.markdown("""
    ### **Option Expiration Payoff Graphs**

    This interactive Streamlit app visualizes the expiration payoffs of European call and put option strategies.
    Users can input calls, puts, and underlying contracts using the input panels below.
    
    The app computes payoffs in real-time and displays key portfolio metrics, including net positions, total cost or premium received, and an approximation of the portfolio's risk profile.

    📌 **Key Features**:
    - Intuitive input fields for Calls, Puts, and Underlying Assets
    - Real-time calculation of net positions and total credit/debit per asset type
    - Instantaneous rendering of the portfolio’s expiration payoff graph
    - Visual and numerical breakdown of position costs and directional exposure
    """)



###! ------------------ Create Expander for Volatility Spread Information ------------------ ### 

with st.expander("ℹ️ About Volatility Spreads", expanded=False):
    st.markdown("""
    **:blue[Volatility Spreads Overview]**  
    Volatility spreads are multi-leg option strategies designed to **profit from changes in implied or realized volatility**, often with **defined risk and reward**.  
    These strategies involve combinations of calls and/or puts at different strikes and quantities, and are commonly used to express **views on market movement magnitude**, **volatility skew**, or **mean reversion** expectations.  

    Below are some of the **most commonly used volatility spread strategies**, each tailored to specific market outlooks and risk profiles. 

    *Note: The information given assumes you are taking a long position in the spread (i.e a net debit position)*
    """)

    tabs = st.tabs([
        "Straddle", 
        "Strangle", 
        "Butterfly Spread", 
        "Iron Condor", 
        "Call Ratio Spread", 
        "Put Ratio Spread", 
        "Call Christmas Tree", 
        "Put Christmas Tree"
    ])

    with tabs[0]:  # Straddle
        st.markdown("""
        **Straddle**  
        - Buy a Call and a Put at the **same strike** and **same expiration**.  
        - Profits from **large moves** in either direction.  
        - Used when expecting **high volatility**, but unsure about direction.  
        - Breakeven: Strike ± total premium paid.  
        - **Risk Profile**: Symmetrical, V-shaped; unlimited upside and downside profit; max loss is the premium.  
        - **Risk Type**: **Limited Risk** (max loss = premium paid).
        """)

    with tabs[1]:  # Strangle
        st.markdown("""
        **Strangle**  
        - Buy a Call and a Put with **different strikes** (typically OTM).  
        - Cheaper than a straddle, but requires a **larger move** to profit.  
        - Useful for directional neutrality with **high volatility expectations**.  
        - Breakeven: Upper and lower strikes ± premiums.  
        - **Risk Profile**: Symmetrical, wider V-shape; unlimited profit potential, max loss equals premium.  
        - **Risk Type**: **Limited Risk**.
        """)

    with tabs[2]:  # Butterfly
        st.markdown("""
        **Butterfly Spread**  
        - Buy 1 lower strike, Sell 2 middle strikes, Buy 1 higher strike.  
        - Profits when the stock ends **near the middle strike**.  
        - Low cost, **defined risk and reward**.  
        - Works best in **low volatility** environments.  
        - **Risk Profile**: Single-peaked (tent-shaped); max profit at center strike, limited loss and gain.  
        - **Risk Type**: **Limited Risk**.
        """)

    with tabs[3]:  # Iron Condor
        st.markdown("""
        **Iron Condor**  
        - Sell 1 OTM Put & 1 OTM Call, Buy 1 further OTM Put & Call.  
        - Net credit strategy, profits if price remains **in a range**.  
        - Good for **low volatility** and time decay.  
        - All risks and profits are capped.  
        - **Risk Profile**: Flat-topped range; max profit between short strikes, defined risk at extremes.  
        - **Risk Type**: **Limited Risk**.
        """)

    with tabs[4]:  # Call Ratio Spread
        st.markdown("""
        **Call Ratio Spread**  
        - Buy 1 Call, Sell **2 or more higher-strike Calls**.  
        - Typically **zero- or low-cost** setup.  
        - Profits if price rises moderately, **losses if it rises too much**.  
        - Used when expecting **limited upside** with low volatility.  
        - **Risk Profile**: Asymmetric; capped profit with potential large loss on strong upside.  
        - **Risk Type**: **Unlimited Risk** (if uncovered).
        """)

    with tabs[5]:  # Put Ratio Spread
        st.markdown("""
        **Put Ratio Spread**  
        - Buy 1 Put, Sell **2 or more lower-strike Puts**.  
        - Profits if price declines **slightly**, but can incur losses if it crashes.  
        - Often used when expecting a **mild drop** or **support level** to hold.  
        - Implied volatility crush can enhance returns.  
        - **Risk Profile**: Asymmetric; capped profit, large potential downside risk.  
        - **Risk Type**: **Unlimited Risk** (if uncovered).
        """)

    with tabs[6]:  # Call Christmas Tree
        st.markdown("""
        **Call Christmas Tree Spread**  
        - Buy 1 ATM Call, Sell 2 slightly higher-strike Calls, Buy 1 further OTM Call.  
        - Asymmetric version of a butterfly.  
        - Low-cost strategy, best if price **drifts upward moderately**.  
        - Designed to profit from **controlled upside** and time decay.  
        - **Risk Profile**: Lopsided peak; capped gain, low or near-zero cost, limited risk.  
        - **Risk Type**: **Limited Risk**.
        """)

    with tabs[7]:  # Put Christmas Tree
        st.markdown("""
        **Put Christmas Tree Spread**  
        - Buy 1 ATM Put, Sell 2 slightly lower-strike Puts, Buy 1 further OTM Put.  
        - Similar to a butterfly, but **more flexible** payoff structure.  
        - Profits from **moderate downward move**, limited risk.  
        - Works well if implied volatility is elevated.  
        - **Risk Profile**: Lopsided tent; capped gain, defined loss, mild bearish outlook.  
        - **Risk Type**: **Limited Risk**.
        """)




st.markdown("""---""")




col1, col2, col3 = st.columns(3, gap="small", border=False)

###! ------------------ Define Option Inputs Form Function ------------------ ###


def asset_input_section(
    asset_type, #set asset type for the inputs to use for string outputs
    session_key, #key to use for updating the dataframes 
    form_key, #key for the form
    col, #col input to distribute widgets and outputs
    default_number, #default number of options
    default_strike, #default strike input
    default_price, #default option price input,
    default_action #0 for Buy, 1 for Sell
):
    
    with col: #choose the column to display the form of inputs
        #* Define the Form
        with st.form(form_key): 
            
            if asset_type in ("Call", "Put"):
                st.subheader(f"{asset_type} Options Inputs")
            elif asset_type == "Underlying Contract":
                st.subheader(f"{asset_type} Inputs")

            form_col1, form_col2 = st.columns(2, gap="small", border=False)  #create 2 columns for the input widget

            with form_col1: #in the 1st column of the form 
                
                #Number of Options Input Widget
                number = st.number_input(   
                    label=f":blue[Number of {asset_type}s]",
                    min_value=1,
                    max_value=10000,
                    step=1,
                    value=default_number,
                    key=f"{session_key}_number",
                    help=f"Choose the number of {asset_type.lower()}s to update portfolio"
                )

                #* buy or Sell Widget
                action = st.radio(
                    f":blue[Select Action]",
                    options=["Buy", "Sell"],
                    index=default_action, #default action | 0 for Buy, 1 for Sell
                    horizontal=True,
                    key=f"{session_key}_action",
                    help=f"Select Buy or Sell for the {asset_type.lower()}s"
                )


            strike = 0.0 #assign strike price so that the underlying input doesn't cause an error
            if asset_type != "Underlying Contract":
                #Strike Price Input Widget
                with form_col2:
                    strike = st.number_input(
                        label=f":blue[Strike Price of {asset_type} Options]",
                        min_value=0.0,
                        step=1.0,
                        format="%.2f",
                        value=default_strike,
                        key=f"{session_key}_strike",
                        help=f"Choose the strike price of the {asset_type.lower()} options"
                    )
                

            #*Asset Price Input Widget
            with form_col2:
                price = st.number_input(
                    label=f":blue[Purchase Price of {asset_type}s (€)]",
                    min_value=0.0,
                    step=0.1,
                    format="%.2f",
                    value=default_price,
                    key=f"{session_key}_price",
                    help=f"Choose the purchase price of the {asset_type.lower()}s"
                )


            #*Submit Button
            submitted = st.form_submit_button(
                label=":green[Press to Update Portfolio]",
                help="Press to update the options portfolio"
            )
            
    # *Initialize session state list if not already done
    if session_key not in st.session_state: #check if the key we pass to the function is in the session state
        st.session_state[session_key] = []

    #*when you press the submit button add the inputs to the data AFTER checking that option and strike prices are not 0
    if submitted:
        if asset_type == "Underlying Contract":
            if price == 0: 
                with col:
                    st.warning("⚠️ Please enter a positive price to continue")
            else:
                st.session_state[session_key].append([asset_type, strike, number, action, price]) #update the data with the inputs
                st.session_state[f"{session_key}_update_msg"] = True #set a flag to show updated message on the next rerun
                st.rerun() #executes the code again from the top without waiting for user input. To show the "updated" message immediately
        else:    
            if strike == 0 or price == 0:
                with col:
                    st.warning("⚠️ Please enter a positive strike and price to continue")
            else:#if we have positive values for strike and price
                st.session_state[session_key].append([asset_type, strike, number, action, price]) #update the data with the inputs
                st.session_state[f"{session_key}_update_msg"] = True #set a flag to show updated message on the next rerun
                st.rerun() #executes the code again from the top without waiting for user input. To show the "updated" message immediately

    #* Success message after update
    if st.session_state.get(f"{session_key}_update_msg", False): #check that the state key exists, if it doesn't return False (instead of raising an error). 
    
    #*We want the default to be False. Only True when you press the submit button
        with col:
            st.write(f"✅ The {asset_type} portfolio has been updated") 
        time.sleep(1) #how long the message will be displayed
        st.session_state[f"{session_key}_update_msg"] = False #set default value to False. We only want it true when the user presses the button
        st.rerun() #Force a code rerun from the top 

    #* Build DataFrame
    portfolio_df = pd.DataFrame(
        data=st.session_state[session_key],
        columns=["Type", "Strike", "Quantity", "Action", "Cost"]
    )

    #* Reset last action
    with col:
        last_action_btn = st.button(
            label=f"Press to Reset Last {asset_type} Action",
            help=f"Press to reset the last {asset_type.lower()}s action",
            key=f"{asset_type}_last_action"
        )

    if last_action_btn:
        if st.session_state[session_key]: #if the state exists
            st.session_state[session_key].pop() #remove the last element (the last input)
            st.session_state[f"{session_key}_last_msg"] = True #flag to show message to inform that last actio has been reset
            st.rerun() #force a code rerun from the top

    if st.session_state.get(f"{session_key}_last_msg", False): #check that key exists and return False if not (instead of raising an error)
        with col:
            st.write(f"✅ The last {asset_type} action has been reset")
        time.sleep(1)
        st.session_state[f"{session_key}_last_msg"] = False #set default message flag to False. We only want it true when the button is pressed
        st.rerun() #force a code rerun from the top


    #* Swap Buy - Sell Button
    input_key = f"{session_key}"
    if st.session_state[input_key]:
        with col:   
            swap_buy_sell = st.button(
            label=":blue[Swap Buy - Sell orders]",
            key=f"{session_key}_swap",
            help="Press to Swap current position Buy and Sell orders. Buy becomes Sell and Sell becomes Buy"
            )

    
        if swap_buy_sell:
            for i, values in enumerate(st.session_state[input_key]):
                if values[3] == "Buy":
                    st.session_state[input_key][i][3] = "Sell"
                elif values[3] == "Sell":
                    st.session_state[input_key][i][3] = "Buy"
            st.rerun()
       


    #* Full reset
    with col:
        reset_all_btn = st.button(
            label=f":red[Press to Reset {asset_type}s]",
            help=f"Press to reset all the {asset_type.lower()} options"
        )

    if reset_all_btn:
        st.session_state[session_key] = []
        st.session_state[f"{session_key}_reset_msg"] = True
        st.rerun()

    if st.session_state.get(f"{session_key}_reset_msg", False):
        with col:
            st.write(f"✅ The {asset_type} portfolio has been reset")
        time.sleep(0.7)
        st.session_state[f"{session_key}_reset_msg"] = False
        st.rerun()

    #* Return the portfolio with the inputs to be assigned to a variable
    return portfolio_df


###! ------------------ Assign Inputs to Portfolios ------------------ ###


#* Create Call Portoflio & Input Widgets
call_portfolio = asset_input_section(
    asset_type="Call",
    session_key="call_inputs",
    form_key="call_option_inputs",
    col=col1,
    default_number=1,
    default_strike=95.0,
    default_price=6.25,
    default_action=0 #buy
)

#* Create Put Portoflio & Input Widgets
put_portfolio = asset_input_section(
    asset_type="Put",
    session_key="put_inputs",
    form_key="put_option_inputs",
    col=col2,
    default_number=2,
    default_strike=105.0,
    default_price=7.75,
    default_action=1 #sell
)


underlying_portfolio = asset_input_section(
    asset_type="Underlying Contract",
    session_key="underlying_inputs",
    form_key="underlying_contract_inputs",
    col=col3,
    default_strike = 0,
    default_number = 2,
    default_price=98.0,
    default_action=1 #buy
    )

st.markdown("""---""")


###! ------------------ Portfolio Descriptive Measures ------------------ ###

###! ------------------ Define Function to Apply to Portfolios to get Summaries ------------------ ###

def portfolio_statistics(portfolio):
    assets_bought_musk = portfolio["Action"] == "Buy"
    assets_bought = portfolio[assets_bought_musk]["Quantity"].sum()

    assets_sold_musk = portfolio["Action"] == "Sell"
    assets_sold = portfolio[assets_sold_musk]["Quantity"].sum()

    net_assets = assets_bought - assets_sold

    amount_paid = portfolio[assets_bought_musk]["Cost"].sum()
    amount_received = portfolio[assets_sold_musk]["Cost"].sum()

    net_amount = amount_received - amount_paid

    asset_type = portfolio["Type"].iloc[0] #Get the first element only because ALL types are the same in each dataframe

    output={
        "assets_bought" : assets_bought,
        "assets_sold" : assets_sold,
        "net_assets" :net_assets,
        "amount_paid" :amount_paid,
        "amount_received" :amount_received,
        "net_amount" : net_amount,
        "asset_type" : asset_type
    }

    return output

#* define variables for portfolio statistics and assign portfolios to default portfolios if no inputs
if not call_portfolio.empty:
    call_stats = portfolio_statistics(call_portfolio)
else:
    call_stats = {}

if not put_portfolio.empty:
    put_stats = portfolio_statistics(put_portfolio)
else:
    put_stats = {}

if not underlying_portfolio.empty:
    underlying_stats = portfolio_statistics(underlying_portfolio)
else:
    underlying_stats = {}


#* set new columns to print portfolio summaries 
col1, col2, col3 = st.columns(3, gap="small")

###! ------------------ Define Function to Print Portfolios Summaries ------------------ ###

def print_stats(portfolio, col):
    with col:
        if not portfolio.empty: 
            st.markdown(":blue[**Input Summary:**]")
            portfolio_stats = portfolio_statistics(portfolio)

            stats_col1, stats_col2 = st.columns(2, gap="small")

            net_assets = portfolio_stats.get("net_assets")
            str_color = "green" if net_assets > 0 else "red" if net_assets < 0 else "gray"
            position_result = "Long" if net_assets > 0 else "Short" if net_assets < 0 else "Neutral"
            net_assets_str = f":{str_color}[Net Position: {position_result} {abs(portfolio_stats.get("net_assets"))} {portfolio_stats.get("asset_type")}s]"

            net_amount = portfolio_stats.get("net_amount")
            color = "green" if net_amount > 0 else "red"
            net_amount_str = f":{color}[Net Amount: €{portfolio_stats.get("net_amount"):.2f}]"
       

            with stats_col1:  
                st.markdown(f"""
                {portfolio_stats.get('asset_type')}s Bought: {portfolio_stats.get('assets_bought')} \n
                {portfolio_stats.get('asset_type')}s Sold: {portfolio_stats.get('assets_sold')} \n 
                {net_assets_str}
                """)
            with stats_col2:
                st.markdown(f"""
                Amount Paid: €{portfolio_stats.get("amount_paid"):.2f} \n
                Amount Received: €{portfolio_stats.get("amount_received"):.2f} \n
                {net_amount_str}
                """)


print_stats(call_portfolio, col1)

print_stats(put_portfolio, col2)

print_stats(underlying_portfolio, col3)

st.markdown("""---""")


###! ------------------ Define Total Portfolio ------------------ ###
total_portfolio = pd.DataFrame(columns=call_portfolio.columns)

if not call_portfolio.empty:
    total_portfolio = pd.concat([total_portfolio, call_portfolio], ignore_index=True)

if not put_portfolio.empty:
    total_portfolio = pd.concat([total_portfolio, put_portfolio], ignore_index=True)


###! ------------------ Calculate Total Option Portfolio Metrics ------------------ ###

#* Calculate unique Stike Prices and Total Slopes/Quantity/Position at each strike
if not total_portfolio.empty:

    ###* ------------------ Change Buy / Sell to 1 / -1  ------------------ ###
    mapped_action = total_portfolio["Action"].map({"Buy":1, "Sell":-1}) #map Buy to 1 and Sell to -1
    mapped_type = total_portfolio["Type"].map({"Call":1, "Put":-1}) #map Call to 1 and Put to -1 

    ###* ------------------ Create Total Position for each option position  ------------------ ###
    total_portfolio["Position"] = total_portfolio["Quantity"] * mapped_action
    total_portfolio["Position_Slope"] = total_portfolio["Position"] * mapped_type

    ###* ------------------ Keep track of initial column number for later loops  ------------------ ###    
    initial_columns = len(total_portfolio.columns) #number of initial columns in DataFrame

    #*Calculate Total SLope for each Strike Price
    strike_slopes = total_portfolio.groupby("Strike")[["Position_Slope", "Quantity", "Position"]].sum()

    #Get the different strike prices
    strikes = total_portfolio["Strike"].sort_values().unique()
    strikes = pd.Series(strikes)


else:
    st.warning("⚠️ Enter an Option to Continue")


###! ------------------ New Columns for the DataFrame based on strike price intervals  ------------------ ###

#* Create Additional Columns to add to DataFrame
columns = [] #we will (add number of strike prices + 1) columns | Below 95, 95-105, Above 105

if not total_portfolio.empty:

    if len(strikes) > 0:
        columns.append(f"Below {min(strikes)}") #below minimum strike 
        for i in range(1, len(strikes)):
            columns.append(f"{strikes[i-1]} - {strikes[i]}") #e.g 95 - 105
        columns.append(f"Above {max(strikes)}") #above max strike 

        number_extra_columns = len(columns) #how many extra columns we add based on different strike prices

    #Insert the extra columns to the DataFrame
    for i in columns:
        total_portfolio.insert(len(total_portfolio.columns), i, np.nan) #start at the final original column and add the columns with NaN values

###! ------------------ Determine if options are ITM / OTM and adjust slopes in the strike intervals  ------------------ ###

#* Add the Slopes based on if the options are ITM / OTM

if not total_portfolio.empty:

    for i in range(len(total_portfolio)): #for each single option position (each row)
        #Find the position of the column that is below the strike price
        position = ((strikes == total_portfolio["Strike"][i]).argmax()) + initial_columns
        #argmax() will find the position in the strikes list that is equal to the strike price

        if total_portfolio["Type"][i] == "Call": #for call options
            total_portfolio.iloc[i, initial_columns :] = 0 # we put 0s initiall on all extra columns
            total_portfolio.iloc[i, position+1 :] = total_portfolio["Position_Slope"][i] #we put the slope of the option position where the option is ITM

        else: #for put options
            total_portfolio.iloc[i, initial_columns:] = total_portfolio["Position_Slope"][i] #we put initially the slope of the option position in all the extra columns
            total_portfolio.iloc[i, position+1 : ] = 0 #we put 0s in the columns where the option is OTM

#* Calculate the Total Underlying Position. It will be used to adjust Total Slopes
#* if an underlying position has been entered by the user
if not underlying_portfolio.empty:
    underlying_position = underlying_stats.get("net_assets")


#* Calculate Total Slopes for each strike price interval
total_slopes = []
#* sum the slopes in each extra column (strike price interval) and add the underlying position slope to adjust it
if not total_portfolio.empty:
    if not underlying_portfolio.empty:
        total_slopes = total_portfolio.iloc[:, - (len(strikes) + 1):].sum() + underlying_position
    else:
        total_slopes = total_portfolio.iloc[:, - (len(strikes) + 1):].sum()


###! ------------------ Calculate Total Option P&Ls at each strike price ------------------ ###

if not total_portfolio.empty:

    #* Calculate Option P&Ls at each strike price 
    option_p_l = pd.Series(index = strikes) #initiate empty Series to add P&Ls at each strike price later

    for strike in strikes: #for every unique strike price
        profit_loss = 0 #initiate P&L to add at each strike price

        for j in range(len(total_portfolio)): #for each row

            itm_amount = abs(total_portfolio["Strike"][j] - strike) #absolute amount by which the option is ITM for each strike price

            if total_portfolio["Type"][j] == "Call": #for call options
                if total_portfolio["Strike"][j] >= strike: #if the call is OTM
                    profit_loss += total_portfolio["Cost"][j] * (-1 * total_portfolio["Position"][j]) # Only add the cost of the option depending on Buy / Sell
                else: #if call is ITM
                    profit_loss += (itm_amount - total_portfolio["Cost"][j]) * total_portfolio["Position"][j] # (ITM amount - cost) * number of options
                
            else: #for put options
                if total_portfolio["Strike"][j] <= strike: #if put is OTM
                    profit_loss += total_portfolio["Cost"][j] * (-1 * total_portfolio["Position"][j]) #only ad the cost of the option depending on Buy / Sell
                else: #if put is ITM
                    profit_loss += (itm_amount - total_portfolio["Cost"][j]) * total_portfolio["Position"][j] # (ITM amount - cost) * number of options
        
        #* add the total option P&L per strike price to the initialized Series
        option_p_l.loc[strike] = profit_loss

        ###! ------------------ Calculate Underlying Portfolio P&L at the Strike Prices ------------------ ###
        if not underlying_portfolio.empty:
            underlying_p_l = pd.Series(index = strikes) #initiate an empty Series that we will later add the P&L for each strike price
        
        #* map Buy / Sell to 1 / -1
            numbered_action = underlying_portfolio["Action"].map({"Buy":1, "Sell":-1})

        #* create new column based on total underlying position for each contract
            underlying_portfolio["Position"] = underlying_portfolio["Quantity"] * numbered_action
        
        else:
            underlying_p_l = pd.Series(0, index = strikes)

        

        #* create columns for each strike price in the underlying portfolio
        #!!! WE ASSUME THAT THE STRIKE PRICE WILL BE THE UNDERLYING PRICE AT MATURITY !!!#
        if not underlying_portfolio.empty:
            for strike in strikes: 
                col_name = f"{int(strike)}" #define column name to be added based on strike price
                if col_name not in underlying_portfolio.columns: #check if a column for that strike price already exists to avoid errors
                    underlying_portfolio.insert(len(underlying_portfolio.columns), col_name, np.nan) #at the end of the DataFrame add NaN columns for each strike price  
                
                for j in range(len(underlying_portfolio)): #for each row
                    underlying_portfolio[col_name][j] = (strike - underlying_portfolio["Cost"][j]) * underlying_portfolio["Position"][j] 
                    #P&L is the (strike price that we assume is underlying price at maturity - price that we bought the asset for) * 1 or -1 depending on Buy / Sell

                # Calculate Total Underlying P&L per Strike Price
                underlying_p_l.loc[strike] = underlying_portfolio[col_name].sum() #create an index value for each strike price and sum profits based on it

###! ------------------ Calculate Total Portfolio P&L at each strike price ------------------ ###
            total_p_l = option_p_l + underlying_p_l
        else:
            total_p_l = option_p_l




###! ------------------ Break-even Points & Check for Option Position Type ------------------ ###

if not total_portfolio.empty:

    #how many times P&L will change sign
    
    #np.sign() will give +- 1 depending if the value is positive or negative
    signs = np.sign(total_p_l)

    #np.diff() will take the difference of i+1 - i each time. We have a sign change when the difference is different from 0 --> If the difference is 0 it means both P&Ls were the same sign 
    sign_changes = np.diff(signs)
    
    p_l_sign_changes = np.count_nonzero(sign_changes)
    p_l_sign_change_flag = False
    if p_l_sign_changes > 0:
        p_l_sign_change_flag = True


    breakeven_points = [] #initiate empty list for BE points

    ##! ------------------ Check for Options Position Types ------------------ ###

    #* Volatility Spread Flags
    option_position = ""

    single_call_flag = False
    single_put_flag = False
    straddle_flag = False
    strangle_flag = False
    butterfly_flag = False
    condor_flag = False
    call_ratio_flag = False
    put_ratio_flag = False
    call_christmass_tree_flag = False
    put_christmass_tree_flag = False

    #* Flag to check if all strikes are equally spaced
    equally_spaced_strikes_flag = False #Flag to check if all strike prices are equally spaced between them

  
    #* create pivot table to calculate call and put quantities per strike
    pivot_table_quantities = total_portfolio.pivot_table(
            index="Strike", columns="Type", values="Quantity", aggfunc="sum", fill_value=0
            )


    options_bought = 0
    options_sold = 0

    if "Call" in total_portfolio["Type"].values:
        call_quantity_per_strike = pivot_table_quantities["Call"] #this returns a series with strike prices in the index and quantities as values per strike for calls
        calls_bought = call_stats["assets_bought"]
        calls_sold = call_stats["assets_sold"]
        total_call_quantity = pivot_table_quantities["Call"].sum() #this returns a scalar with the total quantity of calls
        options_bought += calls_bought
        options_sold += calls_sold
    
    if "Put" in total_portfolio["Type"].values:
        put_quantity_per_strike = pivot_table_quantities["Put"] #this returns a series with strike prices in the index and quantities as values per strike for puts
        puts_bought = put_stats["assets_bought"]
        puts_sold = put_stats["assets_sold"]
        total_put_quantity = pivot_table_quantities["Put"].sum() #this returns a scalar with the total quantity of puts
        options_bought += puts_bought
        options_sold += puts_sold   


    if len(strikes) > 1:
        strike_differences = pivot_table_quantities.index.sort_values().diff()[1:]
        equally_spaced_strikes_flag = (strike_differences == strike_differences[0]).all()

    if underlying_portfolio.empty:
        #* 1 strike price - Both Calls and Puts
        if len(strikes) == 1: #If we have only 1 strike price 
            if total_portfolio["Type"].nunique() == 2: # and both calls and puts in our total portfolio
                #* Check for Straddle    
                if total_call_quantity == total_put_quantity:
                    straddle_flag = True
                    option_position = "Straddle"
        
            elif total_portfolio["Type"].nunique() == 1: #If we only have 1 type of option (single option)
                    #* Check for naked call
                if total_portfolio["Type"].iloc[0] == "Call" and (options_bought == 0 or options_sold == 0): #we only have Call / Put in our "Type" column. So we only need to check the first element
                    single_call_flag = True
                    option_position = "Naked Call"
                elif total_portfolio["Type"].iloc[0] == "Put" and (options_bought == 0 or options_sold == 0):
                    #* check for naked put
                    single_put_flag = True
                    option_position = "Naked Put"

        #* 2 Strikes 
        if len(strikes) == 2: #If we have 2 strikes
            if total_portfolio["Type"].nunique() == 2: #And both calls and puts in our total portfolio
                #* Check for Strangle
                if options_bought != options_sold and (options_bought == 0 or options_sold == 0):
                    strangle_flag = True 
                    option_position = "Strangle"

            elif total_portfolio["Type"].nunique() == 1: #If we have only calls or only puts (ratio spreads)
                if  options_bought != options_sold:
                    if total_portfolio["Type"].iloc[0] == "Call":
                        call_ratio_flag = True
                        option_position = "Call Ratio"
                    else:
                        put_ratio_flag = True
                        option_position = "Put Ratio"
        
        #* 3 Strikes - only Calls or only Puts - equally spaced strikes
        if len(strikes) == 3 and (total_portfolio["Type"].nunique() == 1):
            #* Check for Butterfly
            if (options_bought == options_sold) and equally_spaced_strikes_flag:
                butterfly_flag = True
                option_position = "Butterfly"
            
            #*check for christmass tree
            elif options_bought != options_sold and (options_sold / options_bought == 2 or options_sold / options_bought == 0.5): #we buy (sell) 1 at lower strike price and sell(buy) 2 at 2 higher strike prices
                if total_portfolio["Type"].iloc[0] == "Call":
                    call_christmass_tree_flag = True
                    option_position = "Call Christmass Tree"    
                else:  
                    put_christmass_tree_flag = True
                    option_position = "Put Christmass Tree"
                
        #* 4 Strikes - only Calls or Puts - equally spaced strikes
        if len(strikes) == 4 and total_portfolio["Type"].nunique() == 1:
            #* Check for Condor
            if options_bought == options_sold and strike_differences[0] == strike_differences[-1]:
                condor_flag = True


###! ------------------ Calculate Breakeven Points (BE Points) ------------------ ###

    #! Break Even points if we have a naked Call
    if single_call_flag: #Breakeven for Call = Strike Price + Call Price
        number_breakeven_points = 1
        
        if total_p_l.iloc[0] >= 0: #if we sold the call (negative slope)
            point = strikes.iloc[0] - (abs(total_p_l.iloc[0]) / total_slopes.iloc[1]) # a Call is ITM if price is > strike price so we have a slope above strike price but we will have negative slope so we want subtract a negative number to make it positive
        else: #if we bought the call (positive slope)
            point = strikes.iloc[0] + (abs(total_p_l.iloc[0]) / total_slopes.iloc[1]) # a Call is ITM if price is > strike price so we have a slope above strike price
        breakeven_points.append(point)

    #! Break Even points if we have a naked Put
    elif single_put_flag: #Breakeven for Put = Strike Price - Put Price
        number_breakeven_points = 1
        
        if total_p_l.iloc[0] > 0: #if we sold the put (positive slope)
            point = strikes.iloc[0] - (abs(total_p_l.iloc[0]) / total_slopes.iloc[0]) #Put has a slope if price is below strike price
        else: #if we bought the put (negative slope)
            point = strikes.iloc[0] + (abs(total_p_l.iloc[0]) / total_slopes.iloc[0]) #Put has a slope if price is below strike price
        breakeven_points.append(point)

    #! Break Even points if we have a Straddle
    elif straddle_flag:
        number_breakeven_points = 2
        
        for i in range(number_breakeven_points): #for each breakeven point
            point = strikes.iloc[0] + (abs(total_p_l.iloc[0]) / total_slopes.iloc[i])
            breakeven_points.append(point)

    #! Break Even points if we have a Strangle
    elif strangle_flag:
        number_breakeven_points = 2

        if total_p_l.iloc[0] >= 0:
            point_1 = strikes.iloc[0] - (abs(total_p_l.iloc[0]) / total_slopes.iloc[0]) #we will have 3 slopes (Only the one in the middle will be 0)
            point_2 = strikes.iloc[1] - (abs(total_p_l.iloc[0]) / total_slopes.iloc[2]) #we will have 3 slopes (Only the one in the middle will be 0)
        else:
            point_1 = strikes.iloc[0] + (abs(total_p_l.iloc[0]) / total_slopes.iloc[0]) #we will have 3 slopes (Only the one in the middle will be 0)
            point_2 = strikes.iloc[1] + (abs(total_p_l.iloc[0]) / total_slopes.iloc[2]) #we will have 3 slopes (Only the one in the middle will be 0)
        breakeven_points.append(point_1)
        breakeven_points.append(point_2)

    #! Break Even points if we have a Butterfly
    elif butterfly_flag:
        number_breakeven_points = 2

        if p_l_sign_change_flag:
            if total_p_l.iloc[1] >= 0: #if we sold the middle strike price --> We bought the wings sold the body --> Long Butterfly
                point_1 = strikes.min() + abs(total_slopes.iloc[1] * total_p_l.iloc[0]) # we will have 4 total strike intervals and slopes only in the 2 middle (below min strike and above max strike we are 0 slope)
                point_2 = strikes.max() - abs(total_slopes.iloc[2] * total_p_l.iloc[2]) 
            else: #if we bought the middle strike price --> We sold the wings bought the body --> Short Butterfly
                point_1 = strikes.min() + abs(total_slopes.iloc[1] * total_p_l.iloc[0]) # we will have 4 total strike intervals and slopes only in the 2 middle (below min strike and above max strike we are 0 slope)
                point_2 = strikes.max() - abs(total_slopes.iloc[2] * total_p_l.iloc[2])
            breakeven_points.append(point_1)
            breakeven_points.append(point_2)

    
    #! Break Even points if we have a Condor
    elif condor_flag:
        number_breakeven_points = 2
        if p_l_sign_change_flag:
            if total_p_l.iloc[1] >= 0: #if we sold the middle strike price --> We bought the wings sold the body --> Long Condor
                point_1 = strikes.min() + abs(total_slopes.iloc[1] * total_p_l.iloc[0]) # we will have 5 total strike intervals and slopes only in the 2nd and 4th position (below min strike, above max strike and between wing strikes are 0 slope)
                point_2 = strikes.max() - abs(total_slopes.iloc[3] * total_p_l.iloc[-1])
            else: #if we bought the middle strike price --> We sold the wings bought the body --> Short Butterfly
                point_1 = strikes.min() + abs(total_slopes.iloc[1] * total_p_l.iloc[0]) # we will have 4 total strike intervals and slopes only in the 2 middle (below min strike and above max strike we are 0 slope)
                point_2 = strikes.max() - abs(total_slopes.iloc[3] * total_p_l.iloc[-1])
            breakeven_points.append(point_1)
            breakeven_points.append(point_2)


    #! Break Even points if we have a Call Ratio
    elif call_ratio_flag:
        number_breakeven_points = 2

        if p_l_sign_change_flag:
            point_1 = strikes.min() + abs(total_slopes.iloc[1] * total_p_l.iloc[0]) 
            point_2 = strikes.max() + abs(total_p_l.iloc[1] / total_slopes.iloc[2])
            breakeven_points.append(point_1)
            breakeven_points.append(point_2)
        else:
            point_2 = strikes.max() + abs(total_p_l.iloc[1] / total_slopes.iloc[2])
            breakeven_points.append(point_2)


    #! Break Even points if we have a Put Ratio
    elif put_ratio_flag:
        number_breakeven_points = 2

        if p_l_sign_change_flag:
            point_1 = strikes.max() - abs(total_slopes.iloc[1] * total_p_l.iloc[1]) 
            point_2 = strikes.min() - abs(total_p_l.iloc[0] / total_slopes.iloc[0])
            breakeven_points.append(point_1)
            breakeven_points.append(point_2)
        else:
            point_1 = strikes.max() - abs(total_slopes.iloc[1] * total_p_l.iloc[1])
            point_2 = strikes.min() - abs(total_p_l.iloc[0] / total_slopes.iloc[0])
            breakeven_points.append(point_1)
            breakeven_points.append(point_2)

    

    #! Break Even points if we have a Call Christmass Tree
    elif call_christmass_tree_flag:
        number_breakeven_points = 2

        if p_l_sign_change_flag:
            if total_p_l.iloc[1] >= 0: #if we sold the higher strike price options
                point_1 = strikes.min() + abs(total_p_l.iloc[0] * total_slopes.iloc[1])
                point_2 = strikes.max() + abs(total_p_l.iloc[1] / total_slopes.iloc[-1])
                breakeven_points.append(point_1)
                breakeven_points.append(point_2)
            else:
                point_1 = strikes.min() + abs(total_p_l.iloc[0] * total_slopes.iloc[1])
                point_2 = strikes.max() + abs(total_p_l.iloc[1] / total_slopes.iloc[-1])
                breakeven_points.append(point_1)
                breakeven_points.append(point_2)
        else:
            point_2 = strikes.max() + abs(total_p_l.iloc[1] / total_slopes.iloc[-1])
            breakeven_points.append(point_2)

    elif put_christmass_tree_flag:
        number_breakeven_points = 2

        if p_l_sign_change_flag:
            if total_p_l.iloc[1] >= 0: #if we sold the higher strike price options
                point_1 = strikes.max() - abs(total_p_l.iloc[-1] * total_slopes.iloc[2])
                point_2 = strikes.min() - abs(total_p_l.iloc[0] / total_slopes.iloc[0])
                breakeven_points.append(point_1)
                breakeven_points.append(point_2)
            else:
                point_1 = strikes.max() - abs(total_p_l.iloc[-1] * total_slopes.iloc[2])
                point_2 = strikes.min() - abs(total_p_l.iloc[0] / total_slopes.iloc[0])
                breakeven_points.append(point_1)
                breakeven_points.append(point_2)
        else:
            point_2 = strikes.min() - abs(total_p_l.iloc[0] / total_slopes.iloc[0])
            breakeven_points.append(point_2)


###! ------------------ Consolidate DataFrames to remove duplicate entries and use for Position Text Box ------------------ ###

    options = total_portfolio.copy()

    options_group_cols = ["Type", "Strike", "Cost"] #*assign the columns based on which we will group by
    #as_index = False to return the dataframe with the columns it had instead of a Multiindex
    options_grouped = options.groupby(options_group_cols, as_index=False)
    # .agg() applies sum() in the position column
    options_grouped = options_grouped.agg({"Position" : "sum"})
    #remove any canceled out positions (net position 0) from opposite user inputs
    options_grouped = options_grouped[options_grouped["Position"] != 0]

    #* Do the same for the underlying portfolio
    underlying_group_cols = ["Cost"]
    if not underlying_portfolio.empty:
        underlyings_grouped = underlying_portfolio.groupby(underlying_group_cols, as_index=False)
        # .agg() applies sum() in the position column
        underlyings_grouped = underlyings_grouped.agg({"Position" : "sum"})
        #remove any canceled out positions (net position 0) from opposite user inputs
        underlyings_grouped = underlyings_grouped[underlyings_grouped["Position"] != 0]

    ###! ------------------ Create Text Box with the full Position to Plot on the top left of the Graph ------------------ ###
    position_text_box = ""
 
    for index, row in options_grouped.iterrows(): #? iterrows returns a tuple (index, row). Index is the rows index value and row a Series with the columns and their values for that row
        pos = row["Position"]
        strike  = row["Strike"]
        opt_type = row["Type"]
        cost = row["Cost"]

        if pos > 0:
            position_text_box += f"+{pos} {strike:.1f} {opt_type} -{cost:.2f}  \n"
        else:
            position_text_box += f"{pos} {strike:.1f} {opt_type} {cost:.2f}  \n"


###! ------------------ Create Portfolio Total Metrics ------------------ ### 


###TODO: Create PORTOFLIO SECTION WITH QUICK RISK CALCULATIONS AND SOME GRAPHS

st.subheader(":blue[Portfolio Summary Metrics]")

portfolio_col_1, portfolio_col_2 = st.columns(2, gap="small")


delta_upside_risk = 0 #? Δ upside risk = Net Total Underlyings + Net Calls
delta_downside_risk = 0 #? Δ downside risk = Net Total Underlyings + Net puts 
vega_risk = 0 #? Κ Vega Risk = Total Net Puts + Total Net Calls = Net Total Options

if not call_portfolio.empty:
    delta_upside_risk += call_stats.get("net_assets", 0)
    vega_risk += call_stats.get("net_assets", 0)

if not put_portfolio.empty:
    delta_downside_risk += put_stats.get("net_assets", 0)
    vega_risk += put_stats.get("net_assets", 0)

if not underlying_portfolio.empty:
    delta_upside_risk += underlying_stats.get("net_assets", 0)
    delta_downside_risk += underlying_stats.get("net_assets", 0)

if delta_upside_risk >= 0:
    delta_upside_string = f"⏫ Portfolio Δ Upside Risk: :green[{delta_upside_risk:.1f}] --> :green[Limited] exposure to risk if stock price increases"
else:
    delta_upside_string = f"⏫ Portfolio Δ Upside Risk: :red[{delta_upside_risk:.1f}] --> :red[Unimited] exposure to risk if stock price increases"

if delta_downside_risk <= 0:
    delta_downside_string = f"⏬ Portfolio Δ Downside Risk: :green[{delta_downside_risk:.1f}] --> :green[Limited] exposure to risk if stock price decreases"
else:
    delta_downside_string = f"⏬ Portfolio Δ Downside Risk: :red[{delta_downside_risk:.1f}] --> :red[Unlimited] exposure to risk if stock price decreases"

if vega_risk >= 0:
    vega_risk_string = f"📈 Portfolio Κ Vega Risk: :green[{vega_risk:.1f}] --> :green[Potentially only limited] exposure to risk in the event of volatility explosion"
else:
    vega_risk_string = f"📈 Portfolio Κ Vega Risk: :red[{vega_risk:.1f}] --> :red[Unlimited] exposure to risk in the event of volatility explosion"

if not total_portfolio.empty:

    with portfolio_col_1:

        st.markdown(f"""
        **Approximate Portfolio Risk Profile:**
        - {delta_upside_string}  \n 
        *:gray[Note: We generally want a positive (+) Δ upside risk, otherwise we face unlimited (catastrophic) risk]*
        - {delta_downside_string}  \n
        *:gray[Note: We generally want a negative (-) Δ downside risk, otherwise we face unlimited (catastrophic) risk]*
        - *{vega_risk_string}*  \n
        *:gray[Note: We generally want a positive (+) K vega risk, otherwise we face unlimited (catastrophic) risk]*

        """)


labels = [] #labels for pie chart
sizes = [] #data for pie chart
colors = [] #colors for each label

if not call_portfolio.empty:
    call_count = call_stats.get("assets_bought", 0) + call_stats.get("assets_sold")
    labels.append("Calls")
    sizes.append(call_count)
    colors.append("cornflowerblue")

if not put_portfolio.empty:    
    put_count = put_stats.get("assets_bought", 0) + put_stats.get("assets_sold")
    labels.append("Puts")
    sizes.append(put_count)
    colors.append("lightcoral")

if not underlying_portfolio.empty: 
    underlying_count = underlying_stats.get("assets_bought", 0) + underlying_stats.get("assets_sold")
    labels.append("Underlying Contracts")
    sizes.append(underlying_count)
    colors.append("lightgray")


if not total_portfolio.empty:

    with portfolio_col_2:
            
            portfolio_tabs = st.tabs(
                ["Asset Breakdown",
                 "Number of Options per Strike"])

            with portfolio_tabs[0]: #Asset Breakdown tab
            #* Create a pie chart with the number of asset types 
                def autopct_format(pct, allvals): #? function to show both numbers and percentages
                    absolute = int(round(pct/100.*sum(allvals)))
                    return f"{pct:.1f}%\n({absolute})" 

                fig, ax = plt.subplots(figsize=(15, 4))
                ax.pie(
                    sizes,
                    labels=labels,
                    autopct=lambda pct: autopct_format(pct, sizes),
                    startangle=90,
                    colors=colors,
                    textprops={'fontweight': 'bold'}  #This makes both labels and autopct bold
                )

                plt.legend(loc="upper left")
                ax.axis('equal') #makes the pie chart a circle
                plt.tight_layout()
                st.pyplot(fig)


            with portfolio_tabs[1]: # number of options per strike tab
            #* Create a pie chart with the number of asset types using the pivot table we calculated before
                for col in ["Call", "Put"]:
                    if col not in pivot_table_quantities: #ensure both columns exist otherwise set to 0
                        pivot_table_quantities[col] = 0

                fig, ax = plt.subplots(figsize=(15, 4))
                index = strikes
                x = range(len(strikes))

                bar_width = 0.1
                call_bars = ax.bar([i - bar_width/2 for i in x], pivot_table_quantities['Call'], width=bar_width, label='Calls', color='cornflowerblue')
                put_bars = ax.bar([i + bar_width/2 for i in x], pivot_table_quantities['Put'], width=bar_width, label='Puts', color='lightcoral')


                #* add quantities in bars
                for bar in call_bars:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2, height/2, int(height),
                                ha='center', va='center', fontsize=10, fontweight='bold', color='black')

                for bar in put_bars:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2, height/2, int(height),
                                ha='center', va='center', fontsize=10, fontweight='bold', color='black')

                ax.set_xticks(x)
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax.set_xticklabels(strikes, fontweight='bold') #? rotation=45 if we want them to be side labels
                ax.set_ylabel("Number of Contracts", fontweight='bold')
                ax.set_xlabel("Strike Price", fontweight='bold')
                ax.set_title("Contracts per Strike", fontweight='bold')
                
                ax.legend()
                plt.tight_layout()
                st.pyplot(fig)

st.markdown("""---""")


###! ------------------ Plot Expiration Payoff Graph ------------------ ###

###! ------------------ X-axis Range (Simulate stock prices) ------------------ ###
st.subheader(":blue[Expiration Payoff Graph]")

if not total_portfolio.empty:

    #* Set x-axis range
    if len(strikes) > 1:
        distance = (strikes.max() - strikes.min()) * 3 #set distance equal to 2*range for the x-axis prices
    else:
        distance = strikes.iloc[0] / 1.5
    number_of_ticks = 1000 #how many different intervals between the min and max of the x axis
    
    min_point = strikes.min() - distance
    max_point = strikes.max() + distance
    
    stock_prices = np.linspace(min_point, max_point, number_of_ticks ) #Simulate stock prices x-axis
    
    if len(strikes) > 1:
        segments = len(total_slopes) - 1  #how many different segments we have in the x-axis --> how many lines we have to calculate
    else: 
        segments = len(total_slopes)

###! ------------------ Y-axis Range ------------------ ###

    #* set y-axis limits
    if len(total_p_l) > 1:
        max_y_lim = 1.2*(abs(total_p_l.max()) + abs(total_p_l.min())) #set maximum range on y so that the graph is symmetrical around y=0
        min_y_lim = -1.2*(abs(total_p_l.max()) + abs(total_p_l.min())) #set minimum range on y so that the graph is symmetrical around y=0
    else: #if we only have 1 number in our total P&L set different limits (e.g 1 Option or Straddle)
        max_y_lim = abs(total_p_l.max()) * 3
        min_y_lim = abs(total_p_l.max()) * -3

###! ------------------ Y-axis Range and Profits per Segment ------------------ ###

    #? Graph Explanation
    with st.expander("ℹ️ Graph Description"): 
        st.markdown("""
        This graph illustrates the **expiration payoff** of your option strategy across a wide range of underlying stock prices.

        - The **x-axis** shows possible stock prices at expiration.
        - The **y-axis** represents the total **profit or loss (€)** of your position.
        - The graph is piecewise linear, with **different slopes** between strike prices depending on the option legs you selected.
        - The **dashed horizontal line** represents the zero profit level.
        - **Breakeven points** are highlighted with markers and labeled accordingly.
        - **P&L values** at strike prices are shown in green (profit) or red (loss).

        This visualization helps you understand where your position makes money, breaks even, or loses money at expiration.
        """)


    #* Plot
    plt.figure(figsize = (20,6)) #set the size of the figure

    #* plot the line below minimum strike
    x_axis_below = stock_prices[stock_prices <= strikes.min()]
    line_below_min_strike = total_slopes.iloc[0] * (x_axis_below - strikes.min()) + total_p_l.iloc[0]
    
    plt.plot(x_axis_below, line_below_min_strike, label = f"Below {strikes.min()}, Slope:{total_slopes.iloc[0]}", c="black", linewidth=1.5)

    #* Plot for each segment between strikes prices we calculate the line
    be_point_intervals = []     
    for i in range(len(strikes) - 1):  
        condition = (stock_prices >= strikes.iloc[i]) & (stock_prices <= strikes.iloc[i+1])
        x_range = stock_prices[condition]
        line = total_slopes.iloc[i+1] * (stock_prices[condition] - strikes[i]) + total_p_l.iloc[i]
        
        plt.plot(x_range, line, label=f"{strikes.iloc[i]} - {strikes.iloc[i+1]}, Slope:{total_slopes.iloc[i+1]}", c="black", linewidth=1.5)

    #*plot the line above max strike
    x_axis_above = stock_prices[stock_prices >= strikes.max()]
    line_above_max_strike = total_slopes.iloc[-1] * (x_axis_above - strikes.max()) + total_p_l.iloc[-1]
    plt.plot(x_axis_above, line_above_max_strike, label = f"Above {strikes.max()}, Slope:{total_slopes.iloc[-1]}", c="black", linewidth=1.5)

    plt.ylim(min_y_lim, max_y_lim) #set the range on y axis so that it is symmetrical around y=0

    #*Place the x-axis in the middle of the graph 
    ax = plt.gca() #get the axes of the plot 
    ax.spines['bottom'].set_position(('data', 0)) #set the bottom spine (x-axis) to the point y=0
    ax.spines["bottom"].set_linestyle("dashed") #make the x-axis dashed
    ax.xaxis.set_ticks([]) #remove values from the x-axis
    ax.spines["left"].set_linestyle("dashed") #make the y-axis dashed
    ax.yaxis.set_ticks([0]) #show only the 0 as value in the y-axis
    ax.spines["top"].set_visible(False) #hide the top border
    ax.spines["right"].set_visible(False) #hide the right border
    
    #!plot the breakeven points
    if single_call_flag:
        ax.plot(breakeven_points[0], 0, marker = "o", color="black")
        ax.annotate(f"BE Point: \n{round(breakeven_points[0],2)}", [breakeven_points[0],0], [breakeven_points[0], max_y_lim/8], weight='bold', fontsize=8, horizontalalignment="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif single_put_flag:
        ax.plot(breakeven_points[0], 0, marker = "o", color="black")
        ax.annotate(f"BE Point: \n{round(breakeven_points[0],2)}", [breakeven_points[0],0], [breakeven_points[0], max_y_lim/8], weight='bold', fontsize=8, horizontalalignment="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))    
    elif straddle_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/8], weight='bold', fontsize=8, horizontalalignment="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif strangle_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/8], weight='bold', fontsize=8, horizontalalignment="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif butterfly_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/8], weight='bold', fontsize=8, horizontalalignment="center", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif condor_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/8], weight='bold', fontsize=8, horizontalalignment="center", color="black", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif call_ratio_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/10], weight='bold', fontsize=8, horizontalalignment="center", color="black", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif put_ratio_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/10], weight='bold', fontsize=8, horizontalalignment="center", color="black", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif call_christmass_tree_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/10], weight='bold', fontsize=8, horizontalalignment="center", color="black", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))
    elif put_christmass_tree_flag:
        for i in range(len(breakeven_points)):
            ax.plot(breakeven_points[i], 0, marker = "o", color="black")
            ax.annotate(f"BE Point: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], max_y_lim/10], weight='bold', fontsize=8, horizontalalignment="center", color="black", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3"))


    else:
        if p_l_sign_changes > 0:
            for i in range(len(breakeven_points)):
                ax.plot(breakeven_points[i], 0, marker = "o", color="black")
                ax.annotate(f"BE Point at: \n{round(breakeven_points[i],2)}", [breakeven_points[i],0], [breakeven_points[i], 3], arrowprops = dict(width=0.03, color="black", shrink=0.1), weight='bold', fontsize=8)

    #* Plot P&L at Strike Prices
    for i in range(len(strikes)):
        if total_p_l.iloc[i] < 0: #negative P&L
            plt.text(strikes.iloc[i], total_p_l.iloc[i] + max_y_lim/10, f"{round(total_p_l.iloc[i],2)}€", weight="bold", horizontalalignment = "center", color="firebrick", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3")) # if P&L is negative, give a red color 
        elif total_p_l.iloc[i] > 0: #positive P&L
            plt.text(strikes.iloc[i], total_p_l.iloc[i] + max_y_lim/10, f"{round(total_p_l.iloc[i],2)}€", weight="bold", horizontalalignment = "center", color="green", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3")) #if P&L is positive, give a green color
        else: #0 P&L
            plt.text(strikes.iloc[i], total_p_l.iloc[i], f"{round(total_p_l.iloc[i],2)}€", weight="bold", horizontalalignment = "center", color="dimgray", bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, boxstyle="round,pad=0.3")) #if P&L is positive, give a green color

    #* Plot the option position text in the top left of the graph
    plt.text(stock_prices.min(), max_y_lim, position_text_box, horizontalalignment="left", verticalalignment="top", fontsize=12)

    #* add graph title and axis titles
    if option_position != "":
        plt.title(f"Option Position Parity Graph ({option_position})", c="black", weight="bold")
    else:
        plt.title("Option Position Parity Graph", c="black", weight="bold")
    plt.xlabel("Stock Price", loc = "right", c="black", weight="bold")
    plt.ylabel("Payoff at Expiration", c="black", weight="bold")

    #* plot dashed vertical lines at the strike prices and the strike prices at the bottom of the graph
    for i in strikes:
        plt.axvline(i, min_y_lim, max_y_lim, ls="dashed", color="gray", linewidth = 0.7)
        plt.text(i, min_y_lim, i, horizontalalignment = "center", weight="bold")

    #* Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    #* Add download button
    st.download_button(
        label=":blue[Download Payoff Graph as PNG]",
        data=buf,
        file_name="payoff_graph.png",
        mime="image/png"
    )   

    plt.legend(loc="upper right")
    plt.tight_layout()
    st.pyplot(plt)
