import base64
import dataclasses
from typing import Any, List, Sequence, Union

from chalk._gen.chalk.common.v1.online_query_pb2 import FeatureExpression
from chalk.features import Feature, FeatureWrapper, Resolver
from chalk.features.feature_set import is_features_cls
from chalk.features.underscore_features import NamedUnderscoreExpr, process_named_underscore_expr


@dataclasses.dataclass
class EncodedOutputs:
    string_outputs: List[str]
    feature_expressions_proto: List[FeatureExpression]
    feature_expressions_base64: List[str]  # B64 encoded


def encode_feature_expression_proto(expr: NamedUnderscoreExpr) -> FeatureExpression:
    processed_expr = process_named_underscore_expr(expr)
    return FeatureExpression(
        namespace=expr.fqn.split(".")[0],
        output_column_name=expr.fqn,
        expr=processed_expr._to_proto(),  # pyright: ignore[reportPrivateUsage]
    )


def encode_feature_expression_base64(expr: FeatureExpression) -> str:
    b = expr.SerializeToString(deterministic=True)
    return base64.b64encode(b).decode("utf-8")


def encode_outputs(output: Sequence[Union[str, NamedUnderscoreExpr, Any]]) -> EncodedOutputs:
    """Returns a list of encoded outputs and warnings"""
    string_outputs: List[str] = []
    feature_expressions_base64: List[str] = []
    feature_expressions_proto: List[FeatureExpression] = []
    for o in output:
        if isinstance(o, (Feature, FeatureWrapper)):
            string_outputs.append(str(o))
        elif is_features_cls(o):
            string_outputs.append(o.namespace)
        elif isinstance(o, Resolver):
            string_outputs.append(o.fqn.split(".")[-1])
        elif isinstance(o, NamedUnderscoreExpr):
            fe = encode_feature_expression_proto(o)
            feature_expressions_proto.append(fe)
            feature_expressions_base64.append(encode_feature_expression_base64(fe))
        else:
            string_outputs.append(str(o))
    return EncodedOutputs(
        string_outputs=string_outputs,
        feature_expressions_base64=feature_expressions_base64,
        feature_expressions_proto=feature_expressions_proto,
    )
