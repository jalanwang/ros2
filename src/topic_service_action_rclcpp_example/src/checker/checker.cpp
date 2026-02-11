#include <memory>

#include "checker/checker.hpp"

Checker::Checker(float goal_sum, const rclcpp::NodeOptions & node_options)
: Node("checker", node_options)
{
  arithmetic_action_client_ = rclcpp_action::create_client<ArithmeticChecker>(
    this->get_node_base_interface(),
    this->get_node_graph_interface(),
    this->get_node_logging_interface(),
    this->get_node_waitables_interface(),
    "arithmetic_checker");

  send_goal_total_sum(goal_sum);
}

Checker::~Checker()
{
}

void Checker::send_goal_total_sum(float goal_sum)
{
  using namespace std::placeholders;

  if (!this->arithmetic_action_client_) {
    RCLCPP_WARN(this->get_logger(), "Action client not initialized");
  }

  if (!this->arithmetic_action_client_->wait_for_action_server(std::chrono::seconds(10))) {
    RCLCPP_WARN(this->get_logger(), "Arithmetic action server is not available.");
    return;
  }

  auto goal_msg = ArithmeticChecker::Goal();
  goal_msg.goal_sum = goal_sum;

  auto send_goal_options = rclcpp_action::Client<ArithmeticChecker>::SendGoalOptions();
  send_goal_options.goal_response_callback = std::bind(&Checker::get_arithmetic_action_goal, this, _1);
  send_goal_options.feedback_callback = std::bind(&Checker::get_arithmetic_action_feedback, this, _1, _2);
  send_goal_options.result_callback = std::bind(&Checker::get_arithmetic_action_result, this, _1);
  this->arithmetic_action_client_->async_send_goal(goal_msg, send_goal_options);
}

void Checker::get_arithmetic_action_goal(
  GoalHandleArithmeticChecker::SharedPtr goal_handle)
{
  //auto goal_handle = future.get();
  if (!goal_handle) {
    RCLCPP_WARN(this->get_logger(), "Action goal rejected.");
  } else {
    RCLCPP_INFO(this->get_logger(), "Action goal accepted.");
  }
}

void Checker::get_arithmetic_action_feedback(
  GoalHandleArithmeticChecker::SharedPtr,
  const std::shared_ptr<const ArithmeticChecker::Feedback> feedback)
{
  RCLCPP_INFO(this->get_logger(), "Action feedback: ");
  for (const auto & formula : feedback->formula) {
    RCLCPP_INFO(this->get_logger(), "\t%s ", formula.c_str());
  }
}

void Checker::get_arithmetic_action_result(
  const GoalHandleArithmeticChecker::WrappedResult & result)
{
  switch (result.code) {
    case rclcpp_action::ResultCode::SUCCEEDED:
      RCLCPP_INFO(this->get_logger(), "Action succeeded!");
      RCLCPP_INFO(this->get_logger(), "Action result(all formula): ");
      for (const auto & formula : result.result->all_formula) {
        RCLCPP_INFO(this->get_logger(), "\t%s ", formula.c_str());
      }
      RCLCPP_INFO(this->get_logger(), "Action result(total sum): ");
      RCLCPP_INFO(this->get_logger(), "\t%.2f ", result.result->total_sum);
      break;
    case rclcpp_action::ResultCode::ABORTED:
      RCLCPP_WARN(this->get_logger(), "The action was aborted");
      return;
    case rclcpp_action::ResultCode::CANCELED:
      RCLCPP_WARN(this->get_logger(), "The action was canceled");
      return;
    default:
      RCLCPP_ERROR(this->get_logger(), "Unknown result code");
      return;
  }
  rclcpp::shutdown();
}

