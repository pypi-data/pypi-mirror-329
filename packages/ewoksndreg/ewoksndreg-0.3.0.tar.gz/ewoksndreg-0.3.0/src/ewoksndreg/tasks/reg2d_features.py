from ewokscore.task import Task
from ..io.input_stack import input_context
from ..features import registration

__all__ = ["Reg2DFeatures"]


class Reg2DFeatures(
    Task,
    input_names=["imagestack", "detector", "matcher", "mapper", "transformation_type"],
    optional_input_names=["inputs_are_stacks", "reference"],
    output_names=["transformations", "features", "matches"],
):
    """Use an feature-based registration method to calculate transformations to register the images in the stack."""

    def run(self):
        detector = registration.FeatureDetector.get_subclass(self.inputs.detector)()
        matcher = registration.FeatureMatching.get_subclass(self.inputs.matcher)()
        mapper = registration.FeatureMapping.get_subclass(self.inputs.mapper)(
            self.inputs.transformation_type
        )
        with input_context(
            self.inputs.imagestack,
            inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
        ) as stack:
            features = registration.detect_features(stack, detector)
            matches = registration.match_features(
                stack,
                features,
                matcher,
                reference=self.get_input_value("reference", 0),
            )
            self.outputs.transformations = registration.transformations_from_features(
                matches, mapper
            )
            self.outputs.features = features
            self.outputs.matches = matches
