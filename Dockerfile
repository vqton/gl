FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["src/WebApp/GL.WebApp.csproj", "src/WebApp/"]
COPY ["src/Application/GL.Application.csproj", "src/Application/"]
COPY ["src/Domain/GL.Domain.csproj", "src/Domain/"]
COPY ["src/Infrastructure/GL.Infrastructure.csproj", "src/Infrastructure/"]
RUN dotnet restore "src/WebApp/GL.WebApp.csproj"
COPY . .
WORKDIR "/src/src/WebApp"
RUN dotnet build "GL.WebApp.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "GL.WebApp.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "GL.WebApp.dll"]
