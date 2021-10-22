from dateutil.tz import tzlocal
from PyQt5 import QtCore
import logging as logger
import pandas as pd
import numpy as np

# TODO: optimize dataframe to dict when performance is slow
LOCAL_TIMEZONE = tzlocal()


class UniversalDataModel(QtCore.QAbstractTableModel):
    """
    This is an universal data model that can handle all cases, hopefully.
    """
    def __init__(self, df_=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self.df = df_

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self.df.colums.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

        elif orientation == QtCore.Qt.Vertical:
            try:
                return self.df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self.df.ix[index.row(), index.column()]))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = self.df.index[index.row()]
        col = self.df.columns[index.column()]

        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self.df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self.df.set_value(row, col, value)
        self.dataChanged.emit(index, index, [])
        self.layoutChanged.emit()
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.columns)
    #
    # def new_update_market_data(self, event_):
    #     try:
    #         if event_.symbol not in list(self.asset_map.keys()):
    #             self.asset_map[event_.symbol] = event_
    #             values = [event_.symbol, event_.sectype, event_.bid, event_.midpoint, event_.ask,
    #                       event_.last_price, event_.last_time_update]
    #             df_temp = pd.DataFrame(data=np.asarray(values).reshape(1, -1), columns=self.df.columns)
    #             self.df = self.df.append(df_temp, ignore_index=True)
    #             # self.df = self.df.append(pd.Series(values, index=self.df.columns), ignore_index=True)
    #             self._dic_df[event_.symbol] = [values]
    #             self.layoutChanged.emit()
    #         else:
    #             symbol = event_.symbol
    #             asset = self.asset_map[event_.symbol]
    #             asset.update_all_price_info(event_)
    #             values = [symbol, asset.sectype, asset.bid, asset.midpoint, asset.ask, asset.last_price, asset.last_time_update]
    #             self._dic_df[event_.symbol].append(values)
    #             self.df.loc[(self.df['Symbol'] == symbol), :] = values
    #             self.layoutChanged.emit()
    #
    #     except Exception as ex:
    #         logger.error(ex)
    #
    # def new_update_portfolio_data(self, event_):
    #     try:
    #         for asset, position in event_.positions.items():
    #             if asset not in list(self.asset_map.keys()):
    #                 N = self.rowCount()
    #                 self.insertRow(N)
    #                 self.asset_map[asset] = position
    #                 values = [position.asset.symbol, position.get_market_value(), position.amount,
    #                           position.price,
    #                           position.asset.bid,
    #                           position.asset.midpoint,
    #                           position.asset.ask,
    #                           position.asset.last_price,
    #                           position.cost_basis,
    #                           position.unrealized_pnl,
    #                           position.realized_pnl,
    #                           position.delta,
    #                           position.last_trade_time,
    #                           position.margin_requirement,
    #                           position.commission]
    #                 df_temp = pd.DataFrame(data=np.asarray(values).reshape(1, -1), columns=self.df.columns)
    #                 self.df = self.df.append(df_temp, ignore_index=True)
    #                 self.layoutChanged.emit()
    #
    #             else:
    #                 symbol = asset.symbol
    #                 values = [position.asset.symbol, position.get_market_value(), position.amount,
    #                           position.price,
    #                           position.asset.bid,
    #                           position.asset.midpoint,
    #                           position.asset.ask,
    #                           position.asset.last_price,
    #                           position.cost_basis,
    #                           position.unrealized_pnl,
    #                           position.realized_pnl,
    #                           position.delta,
    #                           position.last_trade_time,
    #                           position.margin_requirement,
    #                           position.commission]
    #                 self.df.loc[(self.df['Symbol'] == symbol), :] = values
    #                 self.layoutChanged.emit()
    #
    #     except Exception as ex:
    #         logger.error(ex)
    #
    # def new_update_strategy_data(self, event_):
    #     try:
    #         if event_.name not in list(self.asset_map.keys()):
    #             self.asset_map[event_.name] = event_
    #
    #             values = [event_.name,
    #                       event_.balance,
    #                       event_.cash_on_hand,
    #                       event_.commission,
    #                       event_.unrealized_pnl + event_.realized_pnl,
    #                       event_.unrealized_pnl,
    #                       event_.realized_pnl,
    #                       event_.last_close,
    #                       event_.sharpe,
    #                       event_.total_ret,
    #                       event_.today_return,
    #                       event_.address,
    #                       event_.id]
    #             df_temp = pd.DataFrame(data=np.asarray(values).reshape(1, -1), columns=self.df.columns)
    #             self.df = self.df.append(df_temp, ignore_index=True)
    #             self.layoutChanged.emit()
    #
    #         else:
    #             values = [event_.name,
    #                       event_.balance,
    #                       event_.cash_on_hand,
    #                       event_.commission,
    #                       event_.unrealized_pnl + event_.realized_pnl,
    #                       event_.unrealized_pnl,
    #                       event_.realized_pnl,
    #                       event_.last_close,
    #                       event_.sharpe,
    #                       event_.total_ret,
    #                       event_.today_return,
    #                       event_.address,
    #                       event_.id]
    #             symbol = values[0]
    #             self.df.loc[(self.df['Name'] == symbol), :] = values
    #             self.layoutChanged.emit()
    #
    #     except Exception as ex:
    #         logger.error(ex)
    #
    # def update_strategy_pnl_data(self, event_):
    #     """
    #     This function intends to update event and update information in the data model
    #     :param event_: namespace object
    #     :return:
    #     """
    #     try:
    #         if self.df.empty:
    #             index_id = 1
    #         else:
    #             index_id = self.df['id'].max()+1
    #
    #         # update event_.date to estern time
    #         event_.date = event_.date.replace(tzinfo=LOCAL_TIMEZONE)
    #         values = [index_id,
    #                   event_.date,
    #                   event_.strategy_id,
    #                   event_.balance,
    #                   event_.total_pnl,
    #                   event_.realized_pnl,
    #                   event_.unrealized_pnl]
    #         df_temp = pd.DataFrame(data=np.asarray(values).reshape(1, -1), columns=self.df.columns)
    #         self.df = self.df.append(df_temp, ignore_index=True)
    #         self.layoutChanged.emit()
    #     except Exception as ex:
    #         logger.error(ex)
    #
    # def update_historical_positions(self, position_df_):
    #     """
    #     process information get from port
    #     :param position_df_: input information
    #     :return:
    #     """
    #     self.df = position_df_
    #     self.layoutChanged.emit()
    #
    # def update_historical_strategies(self, strategy_df_):
    #     """
    #     process information get from port
    #     :param strategy_df_: input information
    #     :return:
    #     """
    #     self.df = strategy_df_
    #     self.layoutChanged.emit()
    #
    # def update_historical_asset(self, asset_df_):
    #     """
    #     process information get from port
    #     :param asset_df_: input information
    #     :return:
    #     """
    #     self.df = asset_df_
    #     self.layoutChanged.emit()
    #
    # def update_historical_strategy_pnl(self, asset_df_):
    #     """
    #     process information get from port
    #     :param asset_df_: input information
    #     :return:
    #     """
    #     self.df = asset_df_
    #     self.df['date'] = pd.to_datetime(self.df['date'])
    #     self.df.date = self.df.date.dt.tz_convert('US/Eastern')
    #     self.df.sort_values(by='date', inplace=True, ascending=True)
    #
    # def update_historical_trades(self, asset_df_):
    #     """
    #             process information get from port
    #             :param asset_df_: input information
    #             :return:
    #             """
    #     self.df = asset_df_
    #
    # def update_historical_orders(self, order):
    #     """
    #     append new order or update old order
    #     :param order: order object sent from arc trader
    #     :return:
    #     """
    #     if order.order_id not in list(self.order_id_map.keys()):
    #         self.order_id_map[order.order_id] = order
    #         values = [order.order_id, order.broker_order_id, order.strategy_id, order.symbol_id, order.type_id,
    #                   order.tif, order.qty, order.price, order.status, order.fill_amt, order.time_created]
    #         df_temp = pd.DataFrame(data=np.asarray(values).reshape(1, -1), columns=self.df.columns, index=[0])
    #         self.df = pd.concat([df_temp, self.df.ix[:]]).reset_index(drop=True)
    #         self.layoutChanged.emit()
    #
    #     else:
    #         order_id = order.order_id
    #         values = [order.order_id, order.broker_order_id, order.strategy_id, order.symbol_id, order.type_id,
    #                   order.tif, order.qty, order.price, order.status, order.fill_amt, order.time_created]
    #         self.df.loc[(self.df['Order ID'] == order_id), :] = values
    #         self.layoutChanged.emit()
    #
    # def set_historical_orders(self, df):
    #     self.df = df.sort_values(by='time_created', ascending=False).reset_index(drop=True)
    #     self.layoutChanged.emit()
    #
    # def set_historical_trades(self, df):
    #     self.df = df.sort_values(by='time_created', ascending=False).reset_index(drop=True)
    #     self.layoutChanged.emit()
    #
    #     # Set up historical strategy data model with information pulled from database
    #
    # def set_historical_strategy(self, df):
    #     self.df = df.drop(columns=['id']).sort_values('date', ascending=False).reset_index(drop=True)
    #     self.layoutChanged.emit()
    #
    #     # Update historical strategy data model with information from Arc Trader
    #
    # def update_historical_strategy(self, event_):
    #     try:
    #         self.df.loc[-1] = event_
    #         self.df.index = self.df.index + 1
    #         self.df.sort_index(inplace=True)
    #         self.layoutChanged.emit()
    #     except Exception as ex:
    #         logger.error(ex)
    #
    # def set_up_open_positions(self, display_df):
    #     self.df = display_df
    #     self.layoutChanged.emit()
