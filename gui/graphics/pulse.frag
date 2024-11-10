#version 440

layout(location=0) in vec2 qt_TexCoord0;
layout(location=0) out vec4 fragColor;
layout(std140, binding=0) uniform buf {
	mat4 qt_Matrix;
	float qt_opacity;

	float time;
	float radius;
	vec2 centre;
	vec2 size;
} ubuf;

vec3 hsb2rgb(in vec3 c)
{
	vec3 rgb = clamp(abs(mod(c.x * 6.0 + vec3(2.0, 0.0, 4.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
	rgb = rgb * rgb * (3.0 - 2.0 * rgb);
	return c.z * mix(vec3(1.0), rgb, c.y);
}

void main()
{
	vec2 p = (qt_TexCoord0 * ubuf.size - ubuf.centre) / ubuf.radius;

	float r = length(p) * 0.9;
	vec3 color = hsb2rgb(vec3(0.24, 0.7, 0.4));

	float a = pow(r, 2.0);
	float b = sin(r * 0.8 - 1.6);
	float c = sin(r - 0.010);
	float s = sin(max(a - ((ubuf.time - 0.166667) / 2.0 - 1.5) * 3.0 + b, 1.0)) * c;

	color *= (abs(1.0 / (s * 10.8)) - 0.4) * min(2.0 - abs(2.0 - ubuf.time * 4), 1.0);
	fragColor = vec4(color, 1.0);
}