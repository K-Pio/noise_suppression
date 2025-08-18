#include "acoustics.hpp"
#pragma once
#include <algorithm>
#include <utility>

namespace acoustics {

double gain_distance(double r, double r0, double rmax, double gmin)
{
    if (r > rmax) return 0.0;
    const double g = 1.0 / std::pow(1.0 + r / r0, 2.0);
    return std::max(gmin, std::min(1.0, g));
}

std::pair<double,double> pan_lr(double src_x, double lst_x, double R)
{
    const double dx = src_x - lst_x;
    double p = 0.5 + dx / (2.0 * R);
    p = std::clamp(p, 0.0, 1.0);
    const double L = std::cos(M_PI_2 * p);
    const double Rv = std::sin(M_PI_2 * p);
    return {L, Rv};
}

double orient(double ax, double ay, double bx, double by, double cx, double cy)
{
    return (bx-ax)*(cy-ay) - (by-ay)*(cx-ax);
}

bool intersects(double ax, double ay, double bx, double by,
                       double cx, double cy, double dx, double dy)
{
    const double o1 = orient(ax,ay,bx,by,cx,cy);
    const double o2 = orient(ax,ay,bx,by,dx,dy);
    const double o3 = orient(cx,cy,dx,dy,ax,ay);
    const double o4 = orient(cx,cy,dx,dy,bx,by);

    if (o1 == 0 && o2 == 0 && o3 == 0 && o4 == 0)
    {
        return false;
    }
    return (o1 * o2 <= 0) && (o3 * o4 <= 0);
}

std::map<std::string, double>smooth_channels(
                const std::map<std::string,double>& channels,
                std::pair<double,double> targets,
                double alpha) 
{
    auto result = channels;
    result["l"] = smooth(channels.at("l"), targets.first,  alpha);
    result["r"] = smooth(channels.at("r"), targets.second, alpha);
    return result;
}

double dist_tuple(std::tuple<double, double> a, std::tuple<double, double> b)
{
    Vec2 va{std::get<0>(a), std::get<1>(a)};
    Vec2 vb{std::get<0>(b), std::get<1>(b)};
    return dist(va, vb);
}

} // namespace acoustics
