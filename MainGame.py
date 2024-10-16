import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import squarify
import random

# Helper function to generate a random company name
def generate_company_name():
    prefixes = ["Tech", "Info", "Data", "Net", "Global", "Next", "Prime", "Eco", "Auto", "Fin","Grand","Prentor","Kadubo","Fresh","West","Dog","Space","Checker","National","Future","Spin","Zip","Umango","Lofty","Coldwater","Prime","Jimper","Chispa","Alleged","Rubber","Qwerty","Trusted","Crow","Dancing"]
    suffixes = ["Corp", "Inc", "Solutions", "Systems", "Industries", "Holdings", "Enterprises", "Technologies", "Group", "Labs", "and Sons","Benefits","Hothaway","Grumble","Moose","Secure","Boost","Smithworks","Premium","Future","Communities","Merlin","Mania","Sciences","Special","Duck Limited","Credit Corp","Quants","Cubed","Beagle","Fire","Foxes","and Daughters"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

# Helper function to generate a ticker symbol from the company name
def generate_ticker(name):
    words = name.split()
    return "".join([word[0] for word in words]).upper()

# Initialize stock data
industries = ["Technology", "Finance", "Healthcare", "Energy", "Consumer Goods", "Utilities", "Telecommunications", "Real Estate","Insurance","Aerospace & Defense","Materials"]
stocks = {}
historical_prices = {}

for _ in range(15):
    name = generate_company_name()
    ticker = generate_ticker(name)
    price = random.randint(10, 100)
    industry = random.choice(industries)
    stocks[ticker] = [name, price, industry]
    historical_prices[ticker] = [price]

portfolio = {ticker: {'quantity': 0, 'total_cost': 0} for ticker in stocks}
balance = 1000.00  # Starting balance

# Variables to manage the pause feature
paused = False

# Helper function to generate a random int that picks 0 99% of the time and between -100 and 100 3% of the time
def special_random():
    if random.randint(1.00, 100.00) <= 99:
        return 0
    else:
        return random.randint(-82.00, 78.00)

def update_prices():
    if not paused:
        # Introduce a 1 in 100 chance for a market crash
        if random.randint(1, 100) == 1:
            crash_drop = random.randint(10, 80)  # Drop between $10 and $80
            for ticker in stocks:
                new_price = max(0, stocks[ticker][1] - crash_drop)
                stocks[ticker][1] = int(new_price)  # Convert to integer
                historical_prices[ticker].append(int(new_price))
        else:
            industry_changes = {industry: random.randint(-2, 2) for industry in industries}
            bankrupt_stocks = []
            
            for ticker, data in list(stocks.items()):  # Use list to avoid runtime error while modifying dictionary
                industry = data[2]
                new_price = max(0, data[1] + industry_changes[industry] + random.randint(-4, 5) + special_random())
                new_price = int(new_price)  # Convert to integer
                if new_price == 0:
                    bankrupt_stocks.append(ticker)
                else:
                    stocks[ticker][1] = new_price
                    historical_prices[ticker].append(new_price)
            
            for ticker in bankrupt_stocks:
                handle_bankruptcy(ticker)
        
        update_labels()
    root.after(1500, update_prices)  # Schedule the next price update in 1.5 seconds

# Function to update the GUI labels
def update_labels():
    for ticker, data in stocks.items():
        stock_labels[ticker].config(text=f"{data[0]} ({data[2]}) [{ticker}]: ${data[1]}")
    balance_label.config(text=f"Balance: ${balance:.0f}")
    for ticker, data in portfolio.items():
        quantity = data['quantity']
        weighted_avg = calculate_weighted_average(ticker)
        portfolio_labels[ticker]['quantity'].config(text=f"{ticker}: {quantity} (WtdAvg: ${weighted_avg:.1f})")


# Function to show the insufficient funds popup
def show_insufficient_funds_popup():
    top = tk.Toplevel()
    top.configure(bg='black')
    top.title("Insufficient Funds")
    
    label = tk.Label(top, text="You don't have enough money to buy this stock.", fg='lime', bg='black', font=("Helvetica", 12))
    label.pack(padx=20, pady=20)
    
    button = tk.Button(top, text="OK", command=top.destroy, fg='white', bg='red', font=("Helvetica", 12))
    button.pack(pady=(0, 20))

# Function to show the no stocks to sell popup
def show_no_stocks_popup():
    top = tk.Toplevel()
    top.configure(bg='black')
    top.title("No Stocks to Sell")
    
    label = tk.Label(top, text="You don't have this stock to sell.", fg='lime', bg='black', font=("Helvetica", 12))
    label.pack(padx=20, pady=20)
    
    button = tk.Button(top, text="OK", command=top.destroy, fg='white', bg='red', font=("Helvetica", 12))
    button.pack(pady=(0, 20))

def show_bankruptcy_popup(ticker):
    company_name = stocks[ticker][0]
    top = tk.Toplevel()
    top.configure(bg='black')
    top.title("Bankruptcy")
    
    label = tk.Label(top, text=f"{company_name} ({ticker}) has gone bankrupt.", fg='lime', bg='black', font=("Helvetica", 12))
    label.pack(padx=20, pady=20)
    
    button = tk.Button(top, text="OK", command=top.destroy, fg='white', bg='red', font=("Helvetica", 12))
    button.pack(pady=(0, 20))

# Function to handle bankrupt stocks
def handle_bankruptcy(ticker):
    # Only proceed with bankruptcy for 33% of the stocks satisfying the condition
    if random.random() > 0.33:
        return
    show_bankruptcy_popup(ticker)  # Show the bankruptcy pop-up

    # Remove GUI elements
    row_index = stock_labels[ticker].grid_info()['row']
    for widget in stock_frame.grid_slaves(row=row_index):
        widget.grid_forget()
    
    # Remove the stock from data structures
    del stocks[ticker]
    del historical_prices[ticker]
    del portfolio[ticker]
    del stock_labels[ticker]
    del portfolio_labels[ticker]

    generate_new_stock(row_index)
    update_ticker()

def generate_new_stock(row_index):
    name = generate_company_name()
    ticker = generate_ticker(name)
    while ticker in stocks:  # Ensure the new ticker is unique
        name = generate_company_name()
        ticker = generate_ticker(name)
    
    price = random.randint(10, 100)
    industry = random.choice(industries)
    stocks[ticker] = [name, price, industry]
    historical_prices[ticker] = [price]
    portfolio[ticker] = {'quantity': 0, 'total_cost': 0}
    
    add_stock_to_gui(ticker, row_index)
    update_ticker()


def add_stock_to_gui(ticker, row_index):
    stock_labels[ticker] = tk.Label(stock_frame, text=f"{stocks[ticker][0]} ({stocks[ticker][2]}) [{ticker}]: ${stocks[ticker][1]}", fg='lime', bg='black', font=("Helvetica", 12))
    stock_labels[ticker].grid(row=row_index, column=0, padx=5, pady=4, sticky='w')
    
    portfolio_labels[ticker] = {'quantity': tk.Label(stock_frame, text=f"{ticker}: {portfolio[ticker]['quantity']} (WtdAvg: ${calculate_weighted_average(ticker):.1f})", fg='white', bg='black', font=("Helvetica", 10))}
    portfolio_labels[ticker]['quantity'].grid(row=row_index, column=1, padx=5, pady=4, sticky='w')
    
    buy_button = tk.Button(stock_frame, text="Buy", command=lambda t=ticker: buy_stock(t, 1), fg='white', bg='green', font=("Helvetica", 10))
    buy_button.grid(row=row_index, column=2, padx=5, pady=4)
    buy_5_button = tk.Button(stock_frame, text="Buy 5", command=lambda t=ticker: buy_stock(t, 5), fg='white', bg='darkgreen', font=("Helvetica", 10))
    buy_5_button.grid(row=row_index, column=3, padx=5, pady=4)
    sell_button = tk.Button(stock_frame, text="Sell", command=lambda t=ticker: sell_stock(t, 1), fg='white', bg='red', font=("Helvetica", 10))
    sell_button.grid(row=row_index, column=4, padx=5, pady=4)
    sell_all_button = tk.Button(stock_frame, text="Sell All", command=lambda t=ticker: sell_all_stock(t), fg='white', bg='darkred', font=("Helvetica", 10))
    sell_all_button.grid(row=row_index, column=5, padx=5, pady=4)
    graph_button = tk.Button(stock_frame, text="Graph", command=lambda t=ticker: plot_stock(t), fg='black', bg='yellow', font=("Helvetica", 10))
    graph_button.grid(row=row_index, column=6, padx=5, pady=4)

# Function to scroll the ticker
def scroll_ticker():
    global ticker_text
    ticker_text = ticker_text[1:] + ticker_text[0]
    ticker_label.config(text=ticker_text)
    root.after(100, scroll_ticker)  # Adjust the speed by changing the time in milliseconds

# Function to update the running ticker
def update_ticker():
    global ticker_text
    ticker_text = " | ".join([f"{ticker}: ${stocks[ticker][1]}" for ticker in stocks])
    ticker_label.config(text=ticker_text)

# Function to handle buying stocks
def buy_stock(ticker, amount=1):
    global balance
    price = stocks[ticker][1]
    total_cost = price * amount
    if balance >= total_cost:
        balance -= total_cost
        portfolio[ticker]['quantity'] += amount
        portfolio[ticker]['total_cost'] += total_cost
        update_labels()
    else:
        show_insufficient_funds_popup()

# Function to handle selling stocks
def sell_stock(ticker, amount=1):
    global balance
    if portfolio[ticker]['quantity'] >= amount:
        price = stocks[ticker][1]
        total_revenue = price * amount
        balance += total_revenue
        portfolio[ticker]['quantity'] -= amount
        portfolio[ticker]['total_cost'] -= amount * price  # Adjust the total cost
        update_labels()
    else:
        show_no_stocks_popup()

def calculate_weighted_average(ticker):
    quantity = portfolio[ticker]['quantity']
    if quantity == 0:
        return 0.0
    total_cost = portfolio[ticker]['total_cost']
    return total_cost / quantity


# Function to handle selling all stocks of a type
def sell_all_stock(ticker):
    global balance
    amount = portfolio[ticker]['quantity']
    if amount > 0:
        price = stocks[ticker][1]
        total_revenue = price * amount
        balance += total_revenue
        portfolio[ticker]['quantity'] = 0
        portfolio[ticker]['total_cost'] = 0  # Reset the total cost
        update_labels()
    else:
        show_no_stocks_popup()

# Function to plot the stock's historical prices
def plot_stock(ticker):
    fig, ax = plt.subplots(figsize=(5, 4))  # Adjust the figsize to make the plot less wide
    ax.plot(historical_prices[ticker], marker='o', linestyle='-', color='lime')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.spines['top'].set_color('gray')
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_color('gray')
    ax.spines['right'].set_color('gray')
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.set_title(f"Historical Prices of {ticker}", color='white')
    ax.set_xlabel("Time", color='white')
    ax.set_ylabel("Price", color='white')
    ax.grid(True, color='gray')
    
    # Clear the previous canvas
    for widget in graph_frame.winfo_children():
        widget.destroy()
    
    # Embed the plot into the tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Close the figure to avoid memory issues
    plt.close(fig)

# Function to plot the market share as a tree map
def plot_market_share():
    fig, ax = plt.subplots(figsize=(5, 4))  # Adjust the figsize to make the plot less wide
    total_market_value = sum(data[1] for data in stocks.values())
    market_shares = [data[1] for data in stocks.values()]
    labels = [f"{ticker}\n{round((data[1] / total_market_value) * 100, 2)}%" for ticker, data in stocks.items()]
    
    colors = [plt.cm.Spectral(i / float(len(labels))) for i in range(len(labels))]
    
    squarify.plot(sizes=market_shares, label=labels, color=colors, alpha=.8, ax=ax)
    ax.set_title("Market Share of Stocks", color='white')
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Clear the previous canvas
    for widget in graph_frame.winfo_children():
        widget.destroy()
    
    # Embed the plot into the tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Close the figure to avoid memory issues
    plt.close(fig)

# Function to plot the total stock market value over time
def plot_total_market_value():
    fig, ax = plt.subplots(figsize=(5, 4))
    total_values = [sum(prices[i] for prices in historical_prices.values() if i < len(prices)) for i in range(len(next(iter(historical_prices.values()))))]
    ax.plot(total_values, marker='o', linestyle='-', color='lime')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.spines['top'].set_color('gray')
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_color('gray')
    ax.spines['right'].set_color('gray')
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.set_title("Total Stock Market Value Over Time", color='white')
    ax.set_xlabel("Time", color='white')
    ax.set_ylabel("Total Value", color='white')
    ax.grid(True, color='gray')

    # Clear the previous canvas
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Embed the plot into the tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Close the figure to avoid memory issues
    plt.close(fig)

# Function to plot a pie chart of the value of current holdings
def plot_holdings():
    fig, ax = plt.subplots(figsize=(5, 4))
    holdings = {ticker: data['quantity'] * stocks[ticker][1] for ticker, data in portfolio.items() if data['quantity'] > 0}
    labels = holdings.keys()
    sizes = holdings.values()

    # Create the pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(holdings))))

    # Add a legend with ticker symbols
    ax.legend(wedges, labels, title="Ticker Symbols", loc="lower center", bbox_to_anchor=(0.5, -0.1), fontsize='small', ncol=3)
    
    # Configure the plot appearance
    ax.set_title("Current Holdings Value", color='white')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.title.set_color('white')

    # Clear the previous canvas
    for widget in graph_frame.winfo_children():
        widget.destroy()
    
    # Embed the plot into the tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Close the figure to avoid memory issues
    plt.close(fig)

# Function to toggle pause/resume
def toggle_pause():
    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")

# Setup the main window
root = tk.Tk()
root.title("Stock Simulator")

# Set the background color to black for Bloomberg-like appearance
root.configure(bg='black')

# Create frames for the buttons, stock list, and the graph
button_frame = tk.Frame(root, bg='black')
button_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='we')

stock_frame = tk.Frame(root, bg='black')
stock_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ns')

graph_frame = tk.Frame(root, bg='black')
graph_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nswe')
graph_frame.grid_propagate(False)  # Prevent the frame from resizing
graph_frame.grid_columnconfigure(1, weight=1)
graph_frame.grid_rowconfigure(1, weight=1)

# Create and place balance label at the top left corner
balance_label = tk.Label(button_frame, text=f"Balance: ${balance}", fg='white', bg='black', font=("Helvetica", 14))
balance_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Create the running ticker label below the balance label
ticker_label = tk.Label(button_frame, text="", fg='lime', bg='black', font=("Helvetica", 12))
ticker_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='we')

# Create and place the market share button at the top
market_share_button = tk.Button(button_frame, text="Market Share", command=plot_market_share, fg='black', bg='yellow', font=("Helvetica", 12))
market_share_button.grid(row=0, column=1, padx=5, pady=5, sticky='e')

# Create and place the total market value button at the top
total_market_value_button = tk.Button(button_frame, text="Total Market Value", command=plot_total_market_value, fg='black', bg='blue', font=("Helvetica", 12))
total_market_value_button.grid(row=0, column=2, padx=2, pady=2, sticky='e')

# Create and place the holdings value button below the stock list
current_holdings_button = tk.Button(button_frame, text="Current Holdings", command=plot_holdings, fg='black', bg='purple', font=("Helvetica", 12))
current_holdings_button.grid(row=0, column=3, padx=2, pady=2, sticky='e')

# Create and place the pause button at the top
pause_button = tk.Button(button_frame, text="Pause", command=toggle_pause, fg='black', bg='red', font=("Helvetica", 12))
pause_button.grid(row=0, column=4, padx=5, pady=5, sticky='e')

# Create and place stock labels with a dark theme
# Create and place stock labels with a dark theme
stock_labels = {}
portfolio_labels = {}

for i, ticker in enumerate(stocks):
    stock_labels[ticker] = tk.Label(stock_frame, text=f"{stocks[ticker][0]} ({stocks[ticker][2]}) [{ticker}]: ${stocks[ticker][1]}", fg='lime', bg='black', font=("Helvetica", 12))
    stock_labels[ticker].grid(row=i, column=0, padx=10, pady=4, sticky='w')
    
    quantity = portfolio[ticker]['quantity']
    weighted_avg = calculate_weighted_average(ticker)
    portfolio_labels[ticker] = {'quantity': tk.Label(stock_frame, text=f"{ticker}: {quantity} (WtdAvg: ${weighted_avg:.1f})", fg='white', bg='black', font=("Helvetica", 10))}
    portfolio_labels[ticker]['quantity'].grid(row=i, column=1, padx=10, pady=6, sticky='e')

    buy_button = tk.Button(stock_frame, text="Buy", command=lambda t=ticker: buy_stock(t, 1), fg='white', bg='green', font=("Helvetica", 10))
    buy_button.grid(row=i, column=2, padx=2, pady=2)
    buy_5_button = tk.Button(stock_frame, text="Buy 5", command=lambda t=ticker: buy_stock(t, 5), fg='white', bg='darkgreen', font=("Helvetica", 10))
    buy_5_button.grid(row=i, column=3, padx=2, pady=2)
    sell_button = tk.Button(stock_frame, text="Sell", command=lambda t=ticker: sell_stock(t, 1), fg='white', bg='red', font=("Helvetica", 10))
    sell_button.grid(row=i, column=4, padx=2, pady=2)
    sell_all_button = tk.Button(stock_frame, text="Sell All", command=lambda t=ticker: sell_all_stock(t), fg='white', bg='darkred', font=("Helvetica", 10))
    sell_all_button.grid(row=i, column=5, padx=2, pady=2)
    graph_button = tk.Button(stock_frame, text="Graph", command=lambda t=ticker: plot_stock(t), fg='black', bg='yellow', font=("Helvetica", 10))
    graph_button.grid(row=i, column=6, padx=2, pady=2)

# Initialize ticker text
ticker_text = ""
update_ticker()

# Update stock prices every 1.5 seconds
root.after(1500, update_prices)
root.after(1000, update_ticker)

# Start the scrolling ticker
scroll_ticker()

# Start the main loop
root.mainloop()
