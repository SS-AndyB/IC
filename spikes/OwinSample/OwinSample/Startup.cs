[assembly: Microsoft.Owin.OwinStartup(typeof(OwinSample.Startup))]

namespace OwinSample
{
    using System;
    using System.Reflection;
    using System.Threading.Tasks;
    using Microsoft.Owin;
    using Owin;

    public class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            app.UseWelcomePage(WelcomePage());

            app.Run(owinContext());
        }

        private static Microsoft.Owin.Diagnostics.WelcomePageOptions WelcomePage()
        {
            return new Microsoft.Owin.Diagnostics.WelcomePageOptions()
            {
                Path = new PathString("/welcome")
            };
        }

        private static Func<IOwinContext, Task> owinContext()
        {
            return context =>
            {
                context.Response.ContentType = "text/plain";

                string output = string.Format(
                    "Welcome to Innovation Club Live!\nI'm running on {0} \nFrom assembly {1}",
                    Environment.OSVersion,
                    Assembly.GetEntryAssembly().FullName
                    );

                return context.Response.WriteAsync(output);
            };
        }
    }
}
