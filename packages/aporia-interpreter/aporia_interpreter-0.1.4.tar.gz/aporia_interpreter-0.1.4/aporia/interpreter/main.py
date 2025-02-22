from aporia.aporia_ast import *
import aporia.interpreter.utils as utils

class InterpLcfi:

  def interp(self, p):
    match p:
      case L_cfi():
        env = {}
        output = []
        for d in p.declar:
          self.interp_declar(d, env)
        for s in p.stmt:
          result = self.interp_stmt(s, env)
          if result:
            output.append(result)
        return "\n".join(output)
      case _:
        raise Exception("Function interp received unexpected object.")

  def interp_declar(self, d, env):
    match d:
      case Declar(Bool(), var_list):
        self.init_variables(var_list, {'type': Bool(), 'value': False}, env)
      case Declar(Int(), var_list):
        self.init_variables(var_list, {'type': Int(), 'value': 0}, env)
      case Declar(Float(), var_list):
        self.init_variables(var_list, {'type': Float(), 'value': 0.0}, env)
      case _:
        raise Exception("Function interp_declar received unexpected object.")

  def init_variables(self, var_list, value, env):
    for v in var_list:
      env[v.name] = value.copy()

  def interp_stmt(self, s, env):
    match s:
      case Stmt(label, pred, inst):
        if self.interp_pred(pred.value, env):
          return self.interp_inst(inst, env)
      case _:
        raise Exception("Function interp_stmt received unexpected object.")

  def interp_pred(self, v, env):
    match v:
      case Bools(value):
        return value
      case Var(name):
        value = env[name]["value"]
        if value is None or not isinstance(env[name]["type"], Bool):
          raise Exception("Prediction variable {} is not a boolean.".format(name))
        return value

  def interp_inst(self, inst, env):
    match inst:
      case AssignInst(assign):
        if assign.var.name in env.keys():
          env[assign.var.name]["value"] = utils.format_for_assign(env[assign.var.name]["type"], self.interp_exp(assign.exp, env))
        else:
          raise Exception("Variable {} was not declared.".format(assign.var.name))
      case PrintInst(string, exp):
        if exp is None and string is None:
          return ""
        else:
          if string is None:
            string = ""
          if exp is None:
            exp = ""
          else:
            exp = utils.format_for_print(self.interp_exp(exp, env))
          return string + exp
      case ExpInst(exp):
        return str(self.interp_exp(exp, env))
      case _:
        raise Exception("Function interp_inst received unexpected object.")
  
  def interp_exp(self, exp, env):
    match exp:
      case Constant(value) | Bools(value):
        return value
      case Var(name):
        return env[name]["value"]
      case UnaryOp(Not(), operand):
        return utils.apply_not(self.interp_exp(operand, env))
      case UnaryOp(USub(), operand):
        return utils.apply_negation(self.interp_exp(operand, env))
      case BinOp(_, BinaryBoolOperator(), _):
        match exp:
          case BinOp(left, And(), right):
            return utils.apply_and(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Or(), right):
            return utils.apply_or(self.interp_exp(left, env), self.interp_exp(right, env))
      case BinOp(_, BinaryNumOperator(), _):
        match exp:
          case BinOp(left, Add(), right):
            return utils.apply_add(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Sub(), right):
            return utils.apply_sub(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Mult(), right):
            return utils.apply_mult(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Div(), right):
            return utils.apply_div(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Mod(), right):
            return utils.apply_mod(self.interp_exp(left, env), self.interp_exp(right, env))
      case BinOp(_, Comparator(), _):
        match exp:
          case BinOp(left, Eq(), right):
            return utils.compare_eq(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Neq(), right):
            return utils.compare_neg(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Ge(), right):
            return utils.compare_ge(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Le(), right):
            return utils.compare_le(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Gt(), right):
            return utils.compare_gt(self.interp_exp(left, env), self.interp_exp(right, env))
          case BinOp(left, Lt(), right):
            return utils.compare_lt(self.interp_exp(left, env), self.interp_exp(right, env))

