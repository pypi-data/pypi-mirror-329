from sqlalchemy import ExecutionContext

class LLMPriceReporter:
    def __init__(self):
        self.total_cost = 0.0
        self.calls = []

    def add_call(self, tag: str,model: str, input_tokens: int, output_tokens: int, cost: float, execution_context: ExecutionContext):
        """
        Add a new LLM call with pre-calculated cost
        
        Args:
            tag (str): Tag of the call
            model (str): Name of the LLM model used
            input_tokens (int): Number of input tokens
            output_tokens (int): Number of output tokens
            cost (float): Pre-calculated cost of the call
        """
        self.calls.append({
            'tag': tag,
            'model': model,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': cost
        })
        self.total_cost += cost

        execution_context.project_context.service_locator.get_llm_logger().log_llm_price(
            tag=tag,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            total_cost=self.total_cost,
            execution_context=execution_context
        )

    def get_report(self) -> str:
        """Generate a formatted cost report"""
        if not self.calls:
            return "No LLM calls recorded."
            
        report = "LLM Usage Report:\n"
        report += "================\n\n"
        
        # Group calls by tag instead of model
        tag_stats = {}
        for call in self.calls:
            tag = call['tag']
            if tag not in tag_stats:
                tag_stats[tag] = {
                    'count': 0,
                    'total_input_tokens': 0,
                    'total_output_tokens': 0,
                    'cost': 0.0
                }
            
            stats = tag_stats[tag]
            stats['count'] += 1
            stats['total_input_tokens'] += call['input_tokens']
            stats['total_output_tokens'] += call['output_tokens']
            stats['cost'] += call['cost']

        # Generate report for each tag
        for tag, stats in tag_stats.items():
            report += f"Tag: {tag}\n"
            report += f"  Calls: {stats['count']}\n"
            report += f"  Total Input Tokens: {stats['total_input_tokens']:,}\n"
            report += f"  Total Output Tokens: {stats['total_output_tokens']:,}\n"
            report += f"  Cost: ${stats['cost']:.4f}\n\n"

        report += f"Total Cost: ${self.total_cost:.4f}"
        return report
