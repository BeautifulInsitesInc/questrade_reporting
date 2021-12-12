from sqlalchemy import Column, String, Integer, Date, ForeignKey, Float, DateTime, Text
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.coercions import TruncatedLabelImpl
from sqlalchemy.sql.expression import column, null
from sqlalchemy.sql.sqltypes import Boolean
from traitlets.traitlets import Int 

Base = declarative_base()

#engine = create_engine('sqlite:///D:\\Dropbox\\code\\riskmit_questrade\\riskmit.db', echo=True)
#Session = sessionmaker(bind=engine) # create a configured "Session" class
#session = Session() # create a Session
#metadata = MetaData(engine)

# ==================================================================
# ================ DATA BASE TABLES ================================
# ==================================================================
class Users(Base):
	__tablename__ = 'users'
	#id = Column(Integer, primary_key=True)
	user_name = Column(String, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)

	def __init__(self, user_name, first_name, last_name):
		self.user_name = user_name
		self.first_name = first_name
		self.last_name = last_name

class Master_accounts(Base):
	__tablename__ = 'master_accounts'
	account_name = Column(String, primary_key=True, nullable=False)
	account_number = Column(Integer, nullable=True)
	owner = Column(String, ForeignKey("users.user_name"),nullable=True)
	broker = Column(String)
	include = Column(Boolean, default=True)

	def __init__(self, account_name, account_number,owner, include, broker):
		self.account_name = account_name
		self.account_number = account_number
		self.owner = owner
		self.broker = broker
		self.include = include

class Accounts(Base):
	__tablename__ = 'accounts'
	type = Column(String)
	number = Column(String,primary_key=True)
	status = Column(String)
	clientAccountType = Column(String)
	master_account_id = Column(String, ForeignKey("master_accounts.account_name"))
	user_id = Column(String, ForeignKey("users.user_name"),nullable=True)
	include = Column(Boolean, default=False,nullable=True)

	def __init__(self, type, number, status, clientAccountType, master_account_id, user_id, include):
		self.type = type
		self.number = number
		self.status = status
		self.clientAccountType = clientAccountType
		self.master_account_id = master_account_id
		self.user_id = user_id
		self.include = include

class Balances(Base):
	__tablename__ = 'balances'
	#id = Column(Integer, autoincrement=True,  primary_key=True)
	currency = Column(String, primary_key=True)
	cash = Column(Integer, primary_key=True)
	marketValue = Column(Integer, primary_key=True)
	totalEquity = Column(Integer, primary_key=True)
	buyingPower = Column(Integer, primary_key=True)
	maintenanceExcess = Column(Integer, primary_key=True)
	account_id = Column(String, ForeignKey("accounts.number"))
	type = Column(String, primary_key=True) # balance or total

	def __init__(self, currency, cash, marketValue, totalEquity, buyingPower, maintenanceExcess, account_id, type):
		self.currency = currency
		self.cash = cash
		self.marketValue = marketValue
		self.totalEquity = totalEquity
		self.buyingPower = buyingPower
		self.maintenanceExcess = maintenanceExcess
		self.account_id = account_id
		self.type = type

class Positions(Base):
	__tablename__ = 'positions'
	symbol = Column(String, primary_key=True)
	symbolId = Column(Integer, primary_key=True)
	openQuantity = Column(Integer, primary_key=True)
	closedQuantity = Column(Integer, primary_key=True)
	currentMarketValue = Column(Float)
	currentPrice = Column(Float)
	averageEntryPrice = Column(Float)
	dayPnl = Column(Float)
	closedPnl = Column(Float)
	openPnl = Column(Float)
	totalCost = Column(Float, primary_key=True)
	isRealTime = Column(Boolean)
	isUnderReorg = Column(Boolean)
	account_id = Column(String, ForeignKey("accounts.number"))

class Orders(Base):
	__tablename__ = 'orders'
	id = Column(String, primary_key=True)
	symbol = Column(String)
	symbolId = Column(String)
	totalQuantity = Column(Float)
	openQuantity = Column(Float)
	filledQuantity = Column(Float)
	canceledQuantity = Column(Float)
	side = Column(String)
	orderType = Column(String)
	limitPrice = Column(Float)
	stopPrice = Column(Float)
	isAllOrNone = Column(Boolean)
	avgExecPrice = Column(Float)
	lastExecPrice = Column(Float)
	timeInForce = Column(String)
	gtdDate = Column(DateTime)
	state = Column(String)
	rejectionReason = Column(Text)
	chainId = Column(String)
	creationTime = Column(DateTime)
	updateTime = Column(DateTime)
	notes = Column(Text)
	commisionCharged = Column(Float)
	userId = Column(String)
	placementCommission = Column(Float)
	triggerStopPrice = Column(Float)
	orderGroupID = Column(String)
	orderClass = Column(String)
	account_id = Column(String, ForeignKey("accounts.number"))

	def __init__(self, id, symbol, symbolId, totalQuantity, openQuantity, filledQuantity, canceledQuantity,	side, orderType, limitPrice, stopPrice, isAllOrNone, avgExecPrice, lastExecPrice, timeInForce, gtdDate,	state, rejectionReason, chainId, creationTime, updateTime, notes, commisionCharged,	userId, placementCommission, triggerStopPrice, orderGroupID, orderClass, account_id):
		self.id = id
		self.symbol = symbol
		self.symbolId = symbolId
		self.totalQuantity = totalQuantity
		self.openQuantity = openQuantity
		self.filledQuantity = filledQuantity
		self.canceledQuantity = canceledQuantity
		self.side = side
		self.orderType = orderType
		self.limitPrice = limitPrice
		self.stopPrice = stopPrice
		self.isAllOrNone = isAllOrNone
		self.avgExecPrice = avgExecPrice
		self.lastExecPrice = lastExecPrice
		self.timeInForce =timeInForce
		self.gtdDate = gtdDate
		self.state = state
		self.rejectionReason = rejectionReason
		self.chainId = chainId
		self.creationTime = creationTime
		self.updateTime = updateTime
		self.notes = notes
		self.commisionCharged = commisionCharged
		self.userId = userId
		self.placementCommission = placementCommission
		self.triggerStopPrice = triggerStopPrice
		self.orderGroupID = orderGroupID
		self.orderClass = orderClass
		self.account_id = account_id

class Executions(Base):
	__tablename__ = 'executions'
	symbol = Column(String)
	symbolId = Column(String)
	quantity = Column(Integer)
	side = Column(String)
	price = Column(Float)
	id = Column(String, primary_key=True)
	orderId = Column(String)
	orderChainId = Column(Integer)
	exchangeExecId = Column(Integer)
	timestamp = Column(DateTime)
	notes = Column(Text)
	venue = Column(String)
	totalCost = Column(Float)
	orderPlacementCommission = Column(Float)
	commission = Column(Float)
	executionFee = Column(Float)
	secFee = Column(Float)
	legId = Column(Float)
	canadianExecutionFee = Column(Float)
	parentId = Column(String)
	account_id = Column(String, ForeignKey("accounts.number"))

	def __init__ (self, symbol,	symbolId, quantity,	side, price, id, orderId, orderChainId,	exchangeExecId,	timestamp, notes, venue, totalCost,	orderPlacementCommission, commission, executionFee,	secFee, legId, canadianExecutionFee, parentId, account_id):
		self.symbol = symbol
		self.symbolId = symbolId
		self.quantity = quantity
		self.side = side
		self.price = price
		self.id = id
		self.orderId = orderId
		self.orderChainId = orderChainId
		self.exchangeExecId = exchangeExecId
		self.timestamp = timestamp
		self.notes = notes
		self.venue = venue
		self.totalCost = totalCost
		self.orderPlacementCommission = orderPlacementCommission
		self.commission = commission
		self.executionFee = executionFee
		self.secFee = secFee
		self.legId = legId
		self.canadianExecutionFee = canadianExecutionFee
		self.parentId = parentId
		self.account_id = account_id

class Activities(Base):
	__tablename__ = 'activities'
	tradeDate = Column(DateTime)
	transactionDate = Column(DateTime)
	settlementDate = column(DateTime)
	action = Column(String, primary_key=True)
	symbol = Column(String, primary_key=True)
	symbolId = Column(String)
	description = Column(String)
	currency = Column(String, primary_key=True)
	quantity = Column(Integer, primary_key=True)
	price = Column(Float)
	grossAmount = Column(Float, primary_key=True)
	commission = Column(Float, primary_key=True)
	netAmount = Column(Float, primary_key=True)
	type = Column(String, primary_key=True)
	account_id = Column(String, ForeignKey("accounts.number"))

	def __init__ (self, tradeDate, transactionDate, settlementDate ,action,symbol, symbolId, description, currency, quantity, price, grossAmount, commission, netAmount, type, account_id):
		self.tradeDate = tradeDate
		self.transactionDate = transactionDate
		self.settlementDate = settlementDate
		self.action = action
		self.symbol = symbol
		self.symbolId = symbolId
		self.description = description
		self.currency = currency
		self.quantity = quantity
		self.price = price
		self.grossAmount = grossAmount
		self.commission = commission
		self.netAmount = netAmount
		self.type = type
		self.account_id = account_id