#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json


class Node():
    '''
    Node 二叉树的节点
    当Node存储值为整数,表示tag id时,为叶子节点
    当Node存储为字符串 '||', '&&', '!'为中间节点,其中值为'!'时,默认只有左孩子节点
    '''

    def __init__(self, nodeValue, leftNode=None, rightNode=None):
        if isinstance(nodeValue, int):
            self.tag = nodeValue
            self.isLeaf = True
            self.leftNode = None
            self.rightNode = None
        elif isinstance(nodeValue, str):
            self.operatorStr = nodeValue
            self.isLeaf = False
            self.leftNode = leftNode
            self.rightNode = rightNode
        else:
            raise Exception('bad node value type:{0} type({1})={2}'.format(nodeValue, nodeValue, type(nodeValue)))

    def get_node_value(self):
        if self.isLeaf:
            return self.tag
        else:
            return self.operatorStr

    def get_left_node(self):
        return self.leftNode

    def get_right_node(self):
        return self.rightNode

    @staticmethod
    def split_logic_exp(exp_str):
        exp_str = exp_str.strip()
        result_list = []
        tmp_item = ''
        is_continue = False
        for c in exp_str:
            if c.isspace():
                if tmp_item:
                    result_list.append(tmp_item)
                    tmp_item = ''
            elif '(' == c or ')' == c:
                if tmp_item:
                    result_list.append(tmp_item)
                    tmp_item = ''
                result_list.append(c)
            elif '&' == c or '|' == c:
                if is_continue:
                    is_continue = False
                    continue

                if tmp_item:
                    result_list.append(tmp_item)
                    tmp_item = ''
                result_list.append(c + c)
                is_continue = True
            elif '!' == c:
                if tmp_item:
                    result_list.append(tmp_item)
                    tmp_item = ''
                result_list.append('!')
            else:
                if not c.isdigit():
                    raise Exception('invalid char {0} in expression {1}'.format(c, exp_str))
                tmp_item += c
        if tmp_item:
            result_list.append(tmp_item)

        return result_list

    @staticmethod
    def merge(op_list, node_list):
        operator_str = op_list.pop()

        if operator_str == '!':
            top = node_list.pop()
            node_list.append(Node('!', leftNode=top))
        else:
            right_node = node_list.pop()
            left_node = node_list.pop()
            node_list.append(Node(operator_str, leftNode=left_node, rightNode=right_node))

    @staticmethod
    def build_logic_tree(item_list):
        operator_set = {'(', ')', '&&', '||', '!'}
        weight_map = {
            '(': 0,
            ')': 0,
            '!': 100,
            '&&': 90,
            '||': 50
        }

        operator_stack = []
        node_stack = []

        for item in item_list:
            if item in operator_set:
                if len(operator_stack) == 0 or '(' == item:
                    operator_stack.append(item)
                elif ')' == item:
                    while '(' != operator_stack[-1]:
                        Node.merge(operator_stack, node_stack)
                        if len(operator_stack) == 0:
                            raise Exception('invalid logic expression ' + ''.join([str(item) for item in item_list]))
                    operator_stack.pop()
                else:
                    if item == '!' and operator_stack[-1] == '!':
                        operator_stack.pop()
                    else:
                        top_weight = weight_map[operator_stack[-1]]
                        current_weight = weight_map[item]
                        if current_weight > top_weight:
                            operator_stack.append(item)
                        else:
                            while len(operator_stack) > 0 and weight_map[operator_stack[-1]] >= current_weight:
                                Node.merge(operator_stack, node_stack)
                            operator_stack.append(item)
            else:
                node_stack.append(Node(int(item)))

        while len(operator_stack) > 0:
            Node.merge(operator_stack, node_stack)
        if len(node_stack) != 1:
            raise Exception('invalid logic express {0}'.format(' '.join([str(item) for item in item_list])))
        return node_stack.pop()

    @staticmethod
    def build_query(node):
        if node.isLeaf:
            return {
                'term': {
                    'tags': node.get_node_value()
                }
            }
        elif '!' == node.get_node_value():
            return {
                'bool': {
                    'must_not': [
                        Node.build_query(node.get_left_node())
                    ]
                }}
        else:
            if '&&' == node.get_node_value():
                return {
                    'bool': {
                        'must': [
                            Node.build_query(node.get_left_node()),
                            Node.build_query(node.get_right_node())
                        ]
                    }
                }
            elif '||' == node.get_node_value():
                return {
                    'bool': {
                        'should': [
                            Node.build_query(node.get_left_node()),
                            Node.build_query(node.get_right_node())
                        ]
                    }
                }

    @staticmethod
    def new_build_query(node, last_operator=None, parent_list=None):
        if node.isLeaf:
            parent_list.append({
                'term': {
                    'tags': node.get_node_value()
                }
            })

        elif '!' == node.get_node_value():
            result_map = {
                'bool': {
                    'must_not': []
                }
            }
            item = Node.new_build_query(node.get_left_node(), '!', result_map['bool']['must_not'])
            if item:
                result_map['bool']['must_not'].append(item)
            return result_map
        elif '&&' == node.get_node_value():
            result_map = None
            if last_operator == '&&':
                tmp_list = parent_list
            else:
                result_map = {
                    'bool': {
                        'must': []
                    }
                }
                tmp_list = result_map['bool']['must']

            item = Node.new_build_query(node.get_left_node(), '&&', tmp_list)
            if item:
                tmp_list.append(item)

            item = Node.new_build_query(node.get_right_node(), '&&', tmp_list)
            if item:
                tmp_list.append(item)
            return result_map
        elif '||' == node.get_node_value():
            result_map = None
            if last_operator == '||':
                tmp_list = parent_list
            else:
                result_map = {
                    'bool': {
                        'should': []
                    }
                }
                tmp_list = result_map['bool']['should']

            item = Node.new_build_query(node.get_left_node(), '||', tmp_list)
            if item:
                tmp_list.append(item)

            item = Node.new_build_query(node.get_right_node(), '||', tmp_list)
            if item:
                tmp_list.append(item)
            return result_map

    @staticmethod
    def parse_logic_exp(exp_str):
        tree_head = Node.build_logic_tree(Node.split_logic_exp(exp_str))
        if tree_head.isLeaf:
            return {
                'bool': {
                    'must': [
                        {
                            'term': {
                                'tags': tree_head.get_node_value()
                            }
                        }
                    ]
                }
            }
        else:
            return Node.new_build_query(tree_head)

    @staticmethod
    def search_without_score(exp_str):
        return {
            'query': {
                'constant_score': {
                    'filter': Node.parse_logic_exp(exp_str)
                }
            }
        }

    @staticmethod
    def search(exp_str):
        return {
            'query': {
                Node.parse_logic_exp(exp_str)
            }
        }


if __name__ == '__main__':
    logic_exp = '11370&&568&&!553'
    #logic_exp = '11370'
    query = Node.search_without_score(logic_exp)

    print(json.dumps(query, indent=2))
