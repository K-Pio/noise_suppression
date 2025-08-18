#pragma once
#include <cmath>
#include <utility>

#include <map>
#include <string>

namespace acoustics {

constexpr double M_PI = 3.14159265358979323846;
constexpr double M_PI_2 = M_PI / 2.0;

double gain_distance(double r, double r0, double rmax, double gmin = 0.02);

std::pair<double,double> pan_lr(double src_x, double lst_x, double R);

double orient(double ax, double ay, double bx, double by, double cx, double cy);

bool intersects(double ax, double ay, double bx, double by,
                       double cx, double cy, double dx, double dy);

inline double smooth(double prev, double target, double alpha)
{
    return prev + alpha * (target - prev);
}

struct Channels
{
    double l;
    double r;
};

std::map<std::string, double>smooth_channels(
                const std::map<std::string,double>& channels,
                std::pair<double,double> targets,
                double alpha);


struct Vec2
{
    double x, y;
};

inline double dist(const Vec2& a, const Vec2& b)
{
    return std::hypot(a.x - b.x, a.y - b.y);
}

double dist_tuple(std::tuple<double, double> a, std::tuple<double, double> b);

} // namespace acoustics
