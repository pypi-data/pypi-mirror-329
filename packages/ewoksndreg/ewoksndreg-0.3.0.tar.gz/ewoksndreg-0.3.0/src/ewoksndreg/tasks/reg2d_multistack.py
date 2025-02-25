from ewokscore.task import Task
from ..io.input_stack import input_context
from ..io.output_stack import output_context, OutputStackNumpy
from ..transformation import apply_transformations
from ..evaluation.evaluation import post_evaluation, pre_evaluation


class Reg2DPreEvaluation(
    Task,
    input_names=["imagestacks"],
    optional_input_names=[
        "inputs_are_stacks",
        "stack_names",
        "preferences",
        "relevant_stacks",
    ],
    output_names=["full_ranking", "ranking", "stack_names"],
):
    """Given several different stacks of images requiring the same alignment, create a ranking of which stacks might be the most suitable to get a correct alignment."""

    def run(self):
        preferences = self.get_input_value("preferences", "")
        stack_names = self.get_input_value("stack_names", [])

        # parse the preferences
        preferred_stacks = []
        for elem in preferences.replace(" ", "").split(","):
            if elem == "":
                continue
            try:
                preferred_stacks.append(int(elem))
            except ValueError:
                if elem not in stack_names:
                    raise ValueError(
                        "The preferred stacks must be specified as a comma-seperated list of either the index or the name(if given) of the stack"
                    )
                preferred_stacks.append(stack_names.index(elem))

        # evaluate all stacks and create ranking
        with input_context(
            self.inputs.imagestacks,
            inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
        ) as stack:
            order = list(pre_evaluation(stack))
            for i in preferred_stacks:
                order.remove(i)
            preferred_stacks.extend(order)

            relevant_stacks = self.get_input_value("relevant_stacks", len(stack))
            self.outputs.ranking = preferred_stacks[:relevant_stacks]
            self.outputs.full_ranking = preferred_stacks
            if stack_names:
                self.outputs.stack_names = [
                    stack_names[i] for i in preferred_stacks[:relevant_stacks]
                ]


class Reg2DPostEvaluation(
    Task,
    input_names=["imagestacks", "transformations"],
    optional_input_names=[
        "url",
        "inputs_are_stacks",
        "chosen_stack",
    ],
    output_names=["imagestacks", "imagestack", "transformations"],
):
    """Given several stacks of images requiring the same alignment and their calculated transformations, determine the stack and list of transformations that resulted in the best registration."""

    def run(self):
        url = self.get_input_value("url", None)
        chosen_stack = self.get_input_value("chosen_stack", -1)
        with output_context(url=url) as ostack:
            with input_context(
                self.inputs.imagestacks,
                inputs_are_stacks=self.get_input_value("inputs_are_stacks", None),
            ) as istacks:
                nstacks = len(self.inputs.transformations)
                if nstacks != istacks.shape[0]:
                    raise ValueError(
                        f"Got {nstacks} lists of transformations and {istacks.shape[0]} imagestacks"
                    )
                transformed = list()
                for index in range(nstacks):
                    out = list()
                    apply_transformations(
                        istacks[index],
                        OutputStackNumpy(out),
                        self.inputs.transformations[index],
                    )
                    transformed.append(out)

                post_eval_rank = post_evaluation(
                    transformed, self.inputs.transformations
                )
                if chosen_stack > -1 and chosen_stack < nstacks:
                    ostack.add_points(transformed[chosen_stack])
                else:
                    ostack.add_points(transformed[post_eval_rank[0]])
            if url:
                self.outputs.imagestack = url
            else:
                self.outputs.imagestack = ostack.data

            self.outputs.imagestacks = transformed
            if chosen_stack < nstacks and chosen_stack > -1:
                self.outputs.transformations = self.inputs.transformations[chosen_stack]
            else:
                self.outputs.transformations = self.inputs.transformations[
                    post_eval_rank[0]
                ]
