# TITRE : PoC avec Open Medic ----
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# VERSION : V4
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# DATE CREATION VERSION PROGRAMME : 12/11/2020
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# AUTEUR : Tim Vlaar
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# CONTEXTE : Maquette Poc en R shiny pour projet ORDEI
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# OBJECTIF : Programme permettant l'affichage de l'outil de visualisation du PoC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# BASES EN ENTREE : 
# - bnpv_open_medic1418_prod_codex : 
# - bnpv_open_medic1418_sa_codex
# - corresp_spe_prod_subs
# - bnpv_eff_soclong_prod_codex_open
# - bnpv_eff_soclong_sa_codex_open
# - bnpv_eff_hlt_prod_codex_open
# - bnpv_eff_hlt_sa_codex_open
# - bnpv_notif_prod_codex_open
# - bnpv_notif_sa_codex_open
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# SORTIES : 
# - Application R shiny
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# 1. LIBRAIRIES ET FONCTIONS ----
library("dplyr")
library("ggplot2")
library("plotly")
library("RColorBrewer")
library("shiny")
library("shinythemes")
library("shinydashboard")
library("shinyBS")
library("stringr")
library("shinyjs")
library("wordcloud2")


# 2. IMPORT DES DONNEES ET PREPARATION ----
# 2.1 Import
bnpv_open_medic1418_prod_codex <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_prod_codex.csv")
bnpv_open_medic1418_sa_codex <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_open_medic1418_sa_codex.csv")
corresp_spe_prod_subs <- read.csv2("~/Documents/GitHub/datamed/ordei/data/corresp_spe_prod_subs.csv")
bnpv_eff_soclong_prod_codex_open <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_prod_codex_open.csv")
bnpv_eff_soclong_sa_codex_open <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_eff_soclong_sa_codex_open.csv")
bnpv_eff_hlt_prod_codex_open <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_prod_codex_open.csv")
bnpv_eff_hlt_sa_codex_open <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_eff_hlt_soclong_sa_codex_open.csv")
bnpv_notif_prod_codex_open <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_notif_prod_codex_open.csv")
bnpv_notif_sa_codex_open <- read.csv2("~/Documents/GitHub/datamed/ordei/data/bnpv_notif_sa_codex_open.csv")


# 2.2 Préparation
# corresp prod_subs
corresp_prod_subs <- corresp_spe_prod_subs %>%
  group_by(PRODUIT_CODEX, SUBSTANCE_CODEX_UNIQUE) %>%
  summarise(n_prod_subs=n()) %>%
  select(-n_prod_subs)

corresp_prod_subs<-na.omit(corresp_prod_subs) # 2 pdts sans substance

# Liste à produits/substances à afficher
list_prod <- as.data.frame(as.character(unique(bnpv_open_medic1418_prod_codex$PRODUIT_CODEX)))
list_prod$TYP_MEDICAMENT <- "Produit"
names(list_prod)[1] <- "MEDICAMENT"
list_prod$MEDICAMENT<-as.character(list_prod$MEDICAMENT)

list_sa <- as.data.frame(as.character(unique(bnpv_open_medic1418_sa_codex$SUBSTANCE_CODEX_UNIQUE)))
list_sa$TYP_MEDICAMENT <- "Substance"
names(list_sa)[1] <- "MEDICAMENT"
list_sa$MEDICAMENT<-as.character(list_sa$MEDICAMENT)

list_prod_sa <- rbind(list_prod,list_sa)
list_prod_sa <- list_prod_sa[order(list_prod_sa$MEDICAMENT),]

# Paramétrage de l'affichage dans la recherche textuelle pour les substances (en gras)
for (i in 1:nrow(list_sa)) {
  a<-paste0(".selectize-dropdown [data-value=\"",list_sa$MEDICAMENT[i],"\"]{ font-weight:bold !important; }")
  if (i==1) {
    param_aff<-a
  } else {
    param_aff<-paste0(param_aff,a)
  }
}

# 3. USER INTERFACE ----
ui <- fluidPage(
  theme = shinytheme("yeti"),h1("ORDEI - Outil d'information des effets indésirables (PoC)"),
  tags$head(tags$style(HTML(param_aff))),
  
  # 3.1 Interface utilisateur pour les choix d'affichage
  fluidRow(
    column(6,
    box(selectInput("select_med", HTML("Saisir le PRODUIT ou la <b>SUBSTANCE ACTIVE</b> :"),
                choices = c("",list_prod_sa$MEDICAMENT), width="400px", multiple = TRUE), width=12),
    box(actionButton("action_rech","Lancer la recherche", width="200px"))),
    column(6,
    box(radioButtons("select_strat", HTML("<b>Choisir un filtre :</b>"), 
               choices=c("Ensemble", "Hommes", "Femmes", "Enfants (0-19 ans)", "Adultes (20-59 ans)", "Séniors (60 ans et plus)"), 
               selected = "Ensemble")), br(), br(),
    box(actionButton(inputId="guide_utilisateur", label="Guide utilisateur"),
        bsModal(id="modal_guide", title="GUIDE UTILISATEUR", "guide_utilisateur", size = "large"))
      )
    ),
  
  # 3.2 Interface utilisateur pour les sorties des indicateurs et graphiques
  fluidRow(box(htmlOutput(outputId = "txt_medicament_choix"), width = 12)),
  
  fluidRow(valueBoxOutput(outputId = "nbre_cas"),
           valueBoxOutput(outputId = "tx_ei")
           ),
  

  fluidRow(box(plotlyOutput("pie_sexe_cas"), width = 3),
           box(plotlyOutput("pie_sexe_conso"), width = 3),
           box(plotlyOutput("pie_age_cas"), width = 3),
           box(plotlyOutput("pie_age_conso"), width = 3)),
  

  fluidRow(column(7, box(plotlyOutput("plot_annee"), width=12), br(), box(plotlyOutput("plot_notif"), width=12)),
  column(5,plotlyOutput("plot_soc_long", height = "750px")))
  

)
  
# 4. SERVER ----
server<-function(input, output){

observeEvent(input$action_rech, { # (si on clique sur "Lancer recherche", faire ce qui suit :)
  
  # 4.1 Définion paramètres choix utilisateur
  med <- input$select_med
  typ_med <- list_prod_sa$TYP_MEDICAMENT[list_prod_sa$MEDICAMENT %in% med]
  strat <- input$select_strat
  
  # 4.2 Sélection des données en fonction des paramètres utilisateur (Produit/Substance)
  if (typ_med=="Substance"){
    data <- bnpv_open_medic1418_sa_codex[bnpv_open_medic1418_sa_codex$SUBSTANCE_CODEX_UNIQUE %in% med,]
    data_soclong <- bnpv_eff_soclong_sa_codex_open[bnpv_eff_soclong_sa_codex_open$SUBSTANCE_CODEX_UNIQUE %in% med,]
    data_notif <- bnpv_notif_sa_codex_open[bnpv_notif_sa_codex_open$SUBSTANCE_CODEX_UNIQUE %in% med,]
    } else {
    data <- bnpv_open_medic1418_prod_codex[bnpv_open_medic1418_prod_codex$PRODUIT_CODEX %in% med,]
    data_soclong <- bnpv_eff_soclong_prod_codex_open[bnpv_eff_soclong_prod_codex_open$PRODUIT_CODEX %in% med,]
    data_notif <- bnpv_notif_prod_codex_open[bnpv_notif_prod_codex_open$PRODUIT_CODEX %in% med,]
   }
  
  # 4.3 Sélection des données en fonction des paramètres utilisateur (Filtres population)
  names(data_soclong)[2]<- "MEDICAMENT"
  names(data_notif)[3]<- "MEDICAMENT"

  if (strat=="Ensemble") {
    data <- data
    data_soclong <- data_soclong
    data_notif <- data_notif
  } else if (strat=="Hommes") {
    data <- data[data$SEXE=="Hommes",]
    data_soclong <- data_soclong[data_soclong$SEXE=="M",]
    data_notif <- data_notif[data_notif$SEXE=="M",]
  } else if (strat=="Femmes") {
    data <- data[data$SEXE=="Femmes",]
    data_soclong <- data_soclong[data_soclong$SEXE=="F",]
    data_notif <- data_notif[data_notif$SEXE=="F",]
  } else if (strat=="Enfants (0-19 ans)") {
    data <- data[data$AGE=="0-19 ans",]
    data_soclong <- data_soclong[data_soclong$AGE==0,]
    data_notif <- data_notif[data_notif$AGE==0,]
  } else if (strat=="Adultes (20-59 ans)") {
    data <- data[data$AGE=="20-59 ans",]
    data_soclong <- data_soclong[data_soclong$AGE==20,]
    data_notif <- data_notif[data_notif$AGE==20,]
  } else if (strat=="Séniors (60 ans et plus)") {
    data <- data[data$AGE=="60 ans et plus",]
    data_soclong <- data_soclong[data_soclong$AGE==60,]
    data_notif <- data_notif[data_notif$AGE==60,]
  }
  
  # Consolidation effets soclong
  temp <- data_soclong %>%
    group_by(MEDICAMENT, SOC_LONG) %>%
    summarise(n_decla_eff=sum(n_decla_eff))
  
  temp2 <- data_soclong %>%
    distinct(MEDICAMENT, AGE, SEXE, n_cas) %>%
    group_by(MEDICAMENT) %>%
    summarise(n_cas=sum(n_cas))
  
  data_soclong <- left_join(temp, temp2, by=c("MEDICAMENT"))
  data_soclong$pour_cas_soclong <- (data_soclong$n_decla_eff/data_soclong$n_cas)*100
  data_soclong<-data_soclong[data_soclong$n_decla_eff>9,]
  data_soclong <- data_soclong[order(data_soclong$pour_cas_soclong, decreasing = TRUE),]

  
  # Consolidation notif
  data_notif <- data_notif %>%
    group_by(MEDICAMENT, TYP_NOTIF) %>%
    summarise(n_decla=sum(n_decla))
  
  
  # 4.4 Sorties indicateurs/graphiques
  # Affichage choix médicament (+ substance associé si produit)
  output$txt_medicament_choix <- renderText({
    if (typ_med=="Substance"){
      paste0(typ_med, " : <font size=5><strong>", med, "</strong></font><br>","Population : <strong>", strat, "</strong>")
    } else {
      paste0(typ_med, " : <font size=5><strong>", med, "</strong></font><br>",
             "Substance(s) active(s) du produit : ","<b>", 
             paste(as.character(corresp_prod_subs$SUBSTANCE_CODEX_UNIQUE[corresp_prod_subs$PRODUIT_CODEX %in% med]),collapse="; "), 
             "</b><br>","Population : <strong>", strat, "</strong>")
    }
    })
  
  # Affichage indicateurs chiffrées (nb cas, patients, taux)
  output$nbre_cas <- renderValueBox({
    if(sum(data$n_cas)==0) {
      valueBox("0 cas déclarés", subtitle = "Nombre de cas déclarés sur la période 2014-2018")
    }else if (sum(data$n_cas)<10) {
      valueBox("< 10 cas déclarés", subtitle = "Nombre de cas déclarés sur la période 2014-2018")
    } else {
    valueBox(paste0(formatC(sum(data$n_cas), big.mark = " ")," cas déclarés"), subtitle = "Nombre de cas déclarés sur la période 2014-2018")
    }
  })
  
  output$tx_ei <- renderValueBox({
    valueBox(paste0(formatC(round((sum(data$n_cas)/sum(data$n_conso))*100000,1), big.mark = " ")," cas /an"), 
             subtitle = "Taux de déclaration pour 100 000 personnes avec une délivrance sur la période 2014-2018")
  })
  
  # Affichage cambemberts âge/sexe des cas/patients
  output$pie_sexe_cas <- renderPlotly({
    data <- data %>%
      group_by(SEXE) %>%
      summarise(n_cas=sum(n_cas))
    
    if (sum(data$n_cas)<10) {
      
    } else {
      cam_sexe_cas <- plot_ly(data, labels = ~as.factor(SEXE), values = ~n_cas, type = 'pie', hole=0.6,sort=FALSE,
                              marker=list(colors=c("#CB181D","#6A51A3"))) %>% 
        layout(margin = list(l = 57, r = 57,b = 57,t = 57), showlegend = FALSE,
               annotations=list(text="Cas déclarés", "showarrow"=F, font=list(size = 11)))
      cam_sexe_cas
      
    }
  })
  
  output$pie_sexe_conso <- renderPlotly({
    data <- data %>%
      group_by(SEXE) %>%
      summarise(n_conso=sum(n_conso))
    
    cam_sexe_conso <- plot_ly(data, labels = ~SEXE, values = ~n_conso, type = 'pie', hole=0.6,sort=FALSE,
                              marker=list(colors=c("#CB181D","#6A51A3"))) %>% 
      layout(margin = list(l = 10, r = 10,b = 10,t = 10),
             annotations=list(text="Patients traités", "showarrow"=F, font=list(size = 11)))
    cam_sexe_conso
  })
  
  
  output$pie_age_cas <- renderPlotly({
    data <- data %>%
      group_by(AGE) %>%
      summarise(n_cas=sum(n_cas))
    
    if (sum(data$n_cas)<10) {
      
    } else {
    cam_age_cas <- plot_ly(data, labels = ~AGE, values = ~n_cas, type = 'pie', hole=0.6,sort=FALSE,
                           marker=list(colors=c("#FFD92F", "#A6D854", "#4EB3D3"))) %>% 
      layout(margin = list(l = 62, r = 62,b = 62,t = 62), showlegend = FALSE,
             annotations=list(text="Cas déclarés", "showarrow"=F, font=list(size = 11)))
    cam_age_cas
    }
  })
  
  
  output$pie_age_conso <- renderPlotly({
    data <- data %>%
      group_by(AGE) %>%
      summarise(n_conso=sum(n_conso))
    
    cam_age_conso <- plot_ly(data, labels = ~AGE, values = ~n_conso, type = 'pie', hole=0.6,sort=FALSE,
                             marker=list(colors=c("#FFD92F", "#A6D854", "#4EB3D3"))) %>% 
      layout(margin = list(l = 0, r = 0,b = 0,t = 0),
             annotations=list(text="Patients traités", "showarrow"=F, font=list(size = 11)))
    cam_age_conso
  })
  
  
  # Histogramme cas/patients par année
  output$plot_annee <- renderPlotly({
    data_annee <- data %>%
      group_by(ANNEE) %>%
      summarise(n_cas=sum(n_cas), n_conso=sum(n_conso))
    
    old.y <- list(side = "left",title = "Nombre de cas d'EI", range=c(0,max(data_annee$n_cas)*1.05), zeroline=TRUE)
    new.y <- list(overlaying = "y",side = "right",showgrid = FALSE,title = "Nombre de patients traités", zeroline=TRUE,range=c(0,max(data_annee$n_conso)*1.05))
    
    if (min(data_annee$n_cas)>9) {
    plot_ly(data=data_annee) %>%
      add_trace(x = ~factor(ANNEE), y = ~n_cas, yaxis = "y1", type="scatter",
                size = 7, name="Cas d'EI", inherit = FALSE, 
                line=list(color='#35978F',width=2),
                marker=list(color='#80CDC1',size=10,
                            line=list(color='#35978F', width=2))) %>%
      add_trace(x = ~factor(ANNEE), y = ~n_conso, yaxis = "y2", type="scatter",
                size = 7, name="Patients traités", inherit = FALSE, 
                line=list(color='#253494',width=2),
                marker=list(color='#1D91C0',size=10,
                            line=list(color='#253494', width=2))) %>%
      layout(yaxis2 = new.y, yaxis = old.y, xaxis = list(title="Année"),
             title="Nombre de cas et patients par année")
      
    } else {
      plot_ly(data=data_annee, x = ~factor(ANNEE), y = ~n_conso, type="scatter",
                  size = 7, name="Patients traités", line=list(color='#253494',width=2),
                  marker=list(color='#1D91C0',size=10,line=list(color='#253494', width=2))) %>%
        layout(title="Nombre de cas et patients par année", xaxis = list(title="Année"),
               showlegend = TRUE, yaxis=list(title = "Nombre de patients traités", zeroline=TRUE,range=c(0,max(data_annee$n_conso)*1.05)))
    }
    
  })

  
  # Histogramme effets SOC_LONG (limité aux 10 premiers)
  output$plot_soc_long <- renderPlotly({
    
    if (nrow(data_soclong)>0) {
    data_soclong <- data_soclong[c(1:10),]
    plot_ly(data=data_soclong, y=~factor(as.character(SOC_LONG), levels = unique(data_soclong$SOC_LONG)[order(data_soclong$pour_cas_soclong)]), 
            x=~round(pour_cas_soclong,1), type = "bar",color =~SOC_LONG,orientation="h", source = "plot_soc_long") %>% 
      layout(showlegend = TRUE, yaxis = list(showticklabels = FALSE, title=""), xaxis = list(ticksuffix="%", title="Pourcentage de cas déclarant l'effet indésirable \n [Cliquez sur les barres pour connaître le détail des effets rapportés]"),
             title="Effets indésirables les plus déclarés par système d'organes", legend = list(orientation = 'h', x=0, y=-0.2),
             margin = list(t = 50))
    } else {
      plot_ly() %>% add_text(x=1,y=1,text="EFFECTIFS TROP FAIBLES POUR AFFICHAGE") %>%
        layout(title="Effets indésirables les plus déclarés par système d'organes")
    } 
  })
  
  # Camembert type de notificateur
  output$plot_notif <- renderPlotly({
    data_notif$TYP_NOTIF <- as.character(data_notif$TYP_NOTIF)
    data_notif$TYP_NOTIF[data_notif$n_decla<10] <- "Notificateur(s) < 10 cas"
    
    plot_ly(data_notif, labels = ~TYP_NOTIF, values = ~n_decla, type = 'pie', 
            hole=0.6,sort=FALSE, marker=list(colors=brewer.pal(length(unique(data_notif$TYP_NOTIF)), "Spectral"))) %>% 
      layout(margin = list(l = 65, r = 65,b = 65,t = 65), showlegend = TRUE,
             title="Répartition des cas déclarés par type de notificateur")

  })
  
  

    
    
  
})
  
# 4.4 Affichage fenêtre avec détail HLT par SOC_LONG 
observeEvent(event_data("plotly_click", source = "plot_soc_long"), { # (si on clique sur une barre SOC_LONG, faire ce qui suit :)
  soc_long_select <- event_data("plotly_click", source = "plot_soc_long") 

    # Paramètres (mêmes que précédemment -> mais à redefinr pour l'observeEvent)
  med <- input$select_med
  typ_med <- list_prod_sa$TYP_MEDICAMENT[list_prod_sa$MEDICAMENT %in% med]
  strat <- input$select_strat
  
  # Données HLT
  if (typ_med=="Substance"){
    data_hlt <- bnpv_eff_hlt_sa_codex_open[bnpv_eff_hlt_sa_codex_open$SUBSTANCE_CODEX_UNIQUE %in% med,]
  } else {
    data_hlt <- bnpv_eff_hlt_prod_codex_open[bnpv_eff_hlt_prod_codex_open$PRODUIT_CODEX %in% med,]
  }
  
  names(data_hlt)[2]<- "MEDICAMENT"
  
  if (strat=="Ensemble") {
    data_hlt <- data_hlt
  } else if (strat=="Hommes") {
    data_hlt <- data_hlt[data_hlt$SEXE=="M",]
  } else if (strat=="Femmes") {
    data_hlt <- data_hlt[data_hlt$SEXE=="F",]
  } else if (strat=="Enfants (0-19 ans)") {
    data_hlt <- data_hlt[data_hlt$AGE==0,]
  } else if (strat=="Adultes (20-59 ans)") {
    data_hlt <- data_hlt[data_hlt$AGE==20,]
  } else if (strat=="Séniors (60 ans et plus)") {
    data_hlt <- data_hlt[data_hlt$AGE==60,]
  }
  
  # Consolidation effets hlt
  data_hlt <- data_hlt %>%
    group_by(MEDICAMENT, EFFET_HLT, SOC_LONG) %>%
    summarise(n_decla_eff_hlt=sum(n_decla_eff_hlt))

  # Sélection des données pour le SOC_LONG sur lequel l'utilisateur a cliqué 
  data_soclong_select <- data_hlt[as.character(data_hlt$SOC_LONG)==soc_long_select$y,]
    
  # Stockage de la sortie (liste des HLT correspondants au SOC_LONG) dans une même chaîne
    for (i in 1 : nrow(data_soclong_select)) {
      if (i==1){
        effets_hlt <- data_soclong_select$EFFET_HLT[i]
      } else {
        effets_hlt <- paste(effets_hlt, data_soclong_select$EFFET_HLT[i], sep = "<br>")
      }
    }
    
  # Affichage d'une fenêtre avec la liste des HLT
    showModal(modalDialog(title = strong(soc_long_select$y), strong("Détail des effets rapportés (par ordre alphabétique) :"), br(),
                          HTML(effets_hlt)))
  })
  
  
}

shinyApp(ui = ui, server = server)

