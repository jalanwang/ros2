#include <cstdio>
#include <memory>
#include <string>
#include <utility>

#include "rclcpp/rclcpp.hpp"
#include "rcutils/cmdline_parser.h"

#include "checker/checker.hpp"


void print_help()
{
  printf("For Node node:\n");
  printf("node_name [-h]\n");
  printf("Options:\n");
  printf("\t-h Help           : Print this help function.\n");
}

int main(int argc, char * argv[])
{
  if (rcutils_cli_option_exist(argv, argv + argc, "-h")) {
    print_help();
    return 0;
  }

  rclcpp::init(argc, argv);

  float goal_total_sum = 50.0;
  char * cli_option = rcutils_cli_get_option(argv, argv + argc, "-g");
  if (nullptr != cli_option) {
    goal_total_sum = std::stof(cli_option);
  }
  printf("goal_total_sum : %2.f\n", goal_total_sum);

  auto checker = std::make_shared<Checker>(goal_total_sum);

  rclcpp::spin(checker);

  rclcpp::shutdown();

  return 0;
}

