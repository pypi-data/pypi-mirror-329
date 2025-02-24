from starknet_py.serialization import Uint256Serializer

from LayerAkira.src.common.ContractAddress import ContractAddress
from LayerAkira.src.common.Requests import Order, IncreaseNonce, CancelRequest, Withdraw
from LayerAkira.src.hasher.types import cancel_all_onchain_type, order_type, cancel_type, cancel_all_type, withdraw_type

u256_serde = Uint256Serializer()


def make_u256_dict(w: int):
    l = u256_serde.serialize(w)
    return {'low': hex(l[0]), 'high': hex(l[1])}


def get_order_typed_data(obj: Order, erc_to_addr, domain, exchange: ContractAddress):
    o = {
        'maker': obj.maker.as_str(), 'price': make_u256_dict(obj.price),
        'qty': {
            'base_qty': make_u256_dict(obj.qty.base_qty),
            'quote_qty': make_u256_dict(obj.qty.quote_qty),
            'base_asset': make_u256_dict(obj.qty.base_asset)
        },
        'base': erc_to_addr[obj.ticker.base].as_str(),
        'quote': erc_to_addr[obj.ticker.quote].as_str(),
        'fee': {
            'trade_fee': {
                'recipient': obj.fee.trade_fee.recipient.as_str(),
                'maker_pbips': obj.fee.trade_fee.maker_pbips,
                'taker_pbips': obj.fee.trade_fee.taker_pbips,
                'apply_to_receipt_amount': obj.fee.trade_fee.apply_to_receipt_amount
            },
            'router_fee': {
                'recipient': obj.fee.router_fee.recipient.as_str(),
                'maker_pbips': obj.fee.router_fee.maker_pbips,
                'taker_pbips': obj.fee.router_fee.taker_pbips,
                'apply_to_receipt_amount': obj.fee.router_fee.apply_to_receipt_amount
            },
            'gas_fee': {
                'gas_per_action': obj.fee.gas_fee.gas_per_action,
                'fee_token': erc_to_addr[obj.fee.gas_fee.fee_token].as_str(),
                'max_gas_price': make_u256_dict(obj.fee.gas_fee.max_gas_price),
                'r0': make_u256_dict(obj.fee.gas_fee.conversion_rate[0]),
                'r1': make_u256_dict(obj.fee.gas_fee.conversion_rate[1]),
            },
        },
        'constraints': {
            'number_of_swaps_allowed': obj.constraints.number_of_swaps_allowed,
            'duration_valid': obj.constraints.duration_valid,
            'created_at': obj.constraints.created_at,
            'stp': str(obj.constraints.stp.value),
            'nonce': obj.constraints.nonce,
            'min_receive_amount': make_u256_dict(obj.constraints.min_receive_amount),
            'router_signer': obj.constraints.router_signer.as_str()
        },
        'salt': hex(obj.salt),
        'flags': {
            'full_fill_only': obj.flags.full_fill_only,
            'best_level_only': obj.flags.best_level_only,
            'post_only': obj.flags.post_only,
            'is_sell_side': obj.flags.is_sell_side,
            'is_market_order': obj.flags.is_market_order,
            'to_ecosystem_book': obj.flags.to_ecosystem_book,
            'external_funds': obj.flags.external_funds,
        },
        'exchange': exchange.as_str(),
        'source': obj.source,
        'sign_scheme': obj.sign_scheme.value
    }
    return {"domain": {"name": domain.name, "version": domain.version,
                       "chainId": hex(domain.chain_id)},
            "types": order_type, "primaryType": "Order", "message": o}


def increase_nonce_typed_data(obj: IncreaseNonce, erc_to_addr, domain):
    return {"domain": {"name": domain.name, "version": domain.version,
                       "chainId": hex(domain.chain_id)},
            "types": cancel_all_onchain_type, "primaryType": "OnchainCancelAll", "message": {
            'maker': obj.maker.as_str(), 'new_nonce': obj.new_nonce, 'salt': hex(obj.salt),
            'gas_fee': {
                'gas_per_action': obj.gas_fee.gas_per_action,
                'fee_token': erc_to_addr[obj.gas_fee.fee_token].as_str(),
                'max_gas_price': make_u256_dict(obj.gas_fee.max_gas_price),
                'r0': make_u256_dict(obj.gas_fee.conversion_rate[0]),
                'r1': make_u256_dict(obj.gas_fee.conversion_rate[1]),
            },
            'sign_scheme': obj.sign_scheme.value
        }}


def cancel_typed_data(obj: CancelRequest, erc_to_addr, domain):
    if obj.order_hash is not None and obj.order_hash != 0:
        data = {"domain": {"name": domain.name, "version": domain.version,
                           "chainId": hex(domain.chain_id)}, "types": cancel_type, "primaryType": "CancelOrder",
                "message": {'maker': obj.maker.as_str(),
                            'order_hash': hex(obj.order_hash),
                            'salt': hex(obj.salt)}
                }
    else:
        data = {"domain": {"name": domain.name, "version": domain.version,
                           "chainId": hex(domain.chain_id)},
                "types": cancel_all_type, "primaryType": "CancelAllOrders",
                "message": {'maker': obj.maker.as_str(),
                            'ticker': {
                                'base': erc_to_addr[obj.exchange_ticker.pair.base].as_str(),
                                'quote': erc_to_addr[obj.exchange_ticker.pair.quote].as_str(),
                                'to_ecosystem_book': obj.exchange_ticker.is_ecosystem_book,
                            },
                            'salt': hex(obj.salt)}}
    return data


def withdraw_typed_data(withdraw: Withdraw, erc_to_addr, domain, exchange: ContractAddress):
    gas_fee = withdraw.gas_fee
    return {"domain": {"name": domain.name, "version": domain.version, "chainId": hex(domain.chain_id)},
            "types": withdraw_type, "primaryType": "Withdraw", "message": {
            'maker': withdraw.maker.as_str(),
            'token': erc_to_addr[withdraw.token].as_str(),
            'amount': make_u256_dict(withdraw.amount),
            'salt': hex(withdraw.salt),
            'gas_fee': {
                'gas_per_action': gas_fee.gas_per_action,
                'fee_token': erc_to_addr[gas_fee.fee_token].as_str(),
                'max_gas_price': make_u256_dict(gas_fee.max_gas_price),
                'r0': make_u256_dict(gas_fee.conversion_rate[0]), 'r1': make_u256_dict(gas_fee.conversion_rate[1])
            },
            'receiver': withdraw.receiver.as_str(),
            'exchange': exchange.as_str(),
            'sign_scheme': withdraw.sign_scheme.value
        }}
